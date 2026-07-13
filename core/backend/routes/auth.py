"""Rutas de autenticación y gestión de licencias."""
import os
import secrets
from fastapi import APIRouter, HTTPException, Depends, Request
from core.backend.dependencies.database import db
from core.backend.dependencies.security import (
    hash_password, verify_password, create_access_token, get_current_admin
)
from core.backend.models.auth import LoginInput, Licencia
from shared.backend.utils import new_id, now_iso

router = APIRouter(prefix="/api/auth")


@router.post("/login")
async def auth_login(data: LoginInput):
    """Login de administrador."""
    user = await db.users.find_one({"email": data.email.lower().strip()})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Credenciales incorrectas")
    token = create_access_token(user["id"], user["email"])
    return {
        "token": token,
        "user": {
            "email": user["email"],
            "name": user.get("name", ""),
            "role": user["role"]
        }
    }


@router.get("/me")
async def auth_me(admin: dict = Depends(get_current_admin)):
    """Devuelve el usuario autenticado."""
    return admin


# ---- Licencias ----
licencias_router = APIRouter(prefix="/api/admin/licencias")


def _gen_license_key() -> str:
    """Genera una clave de licencia tipo NEXO-XXXX-XXXX."""
    return "NEXO-" + secrets.token_hex(4).upper() + "-" + secrets.token_hex(2).upper()


@licencias_router.post("")
async def crear_licencia(data: dict, admin: dict = Depends(get_current_admin)):
    """Crea una nueva licencia (solo admin)."""
    doc = {
        "id": new_id(),
        "license_key": _gen_license_key(),
        "empresa": data.get("empresa", ""),
        "email": data.get("email", ""),
        "telefono": data.get("telefono", ""),
        "precio_mensual": data.get("precio_mensual", 29),
        "estado": "activa",
        "sector": data.get("sector", "taller"),
        "modulos": data.get("modulos", []),
        "notas": data.get("notas", ""),
        "created_at": now_iso(),
    }
    await db.licencias.insert_one(doc)
    return doc


@licencias_router.get("")
async def listar_licencias(admin: dict = Depends(get_current_admin)):
    """Lista todas las licencias."""
    return await db.licencias.find({}, {"_id": 0}).sort("created_at", -1).to_list(200)


@licencias_router.get("/verificar/{license_key}")
async def verificar_licencia(license_key: str):
    """Endpoint público: verifica si una licencia está activa."""
    lic = await db.licencias.find_one({"license_key": license_key}, {"_id": 0})
    if not lic:
        return {"valida": False, "estado": "no_encontrada", "mensaje": "Licencia no válida."}
    activa = lic["estado"] == "activa"
    return {
        "valida": activa,
        "estado": lic["estado"],
        "empresa": lic["empresa"],
        "sector": lic.get("sector", "taller"),
        "mensaje": "Licencia activa." if activa else "Aplicación desactivada. Contacte con su proveedor.",
    }
