"""Rutas CRUD para Clientes y Proveedores."""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from core.backend.dependencies.database import db
from core.backend.models.contacto import Contacto, ContactoInput
from shared.backend.utils import now_iso

router = APIRouter(prefix="/api/contactos")


def clean(doc: dict) -> dict:
    """Elimina _id de MongoDB del documento."""
    doc.pop('_id', None)
    return doc


@router.post("")
async def crear_contacto(data: ContactoInput):
    """Crea un nuevo cliente o proveedor."""
    contacto = Contacto(**data.model_dump())
    await db.contactos.insert_one(contacto.model_dump())
    return contacto.model_dump()


@router.get("")
async def listar_contactos(tipo: Optional[str] = None):
    """Lista contactos. Filtra por tipo (cliente/proveedor) opcionalmente."""
    q = {}
    if tipo:
        q['tipo'] = tipo
    docs = await db.contactos.find(q, {"_id": 0}).sort("created_at", -1).to_list(200)
    return docs


@router.get("/{contacto_id}")
async def obtener_contacto(contacto_id: str):
    """Obtiene un contacto por su ID."""
    doc = await db.contactos.find_one({"id": contacto_id}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "Contacto no encontrado")
    return doc


@router.put("/{contacto_id}")
async def actualizar_contacto(contacto_id: str, data: ContactoInput):
    """Actualiza un contacto existente."""
    res = await db.contactos.update_one(
        {"id": contacto_id}, 
        {"$set": {**data.model_dump(), "updated_at": now_iso()}}
    )
    if res.matched_count == 0:
        raise HTTPException(404, "Contacto no encontrado")
    return await db.contactos.find_one({"id": contacto_id}, {"_id": 0})


@router.delete("/{contacto_id}")
async def eliminar_contacto(contacto_id: str):
    """Elimina un contacto."""
    await db.contactos.delete_one({"id": contacto_id})
    return {"ok": True}
