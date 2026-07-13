"""Punto de entrada de la API FastAPI - NEXOPRO PLATFORM."""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from core.backend.routes import contactos, auth
from core.backend.dependencies.database import db
from core.backend.dependencies.security import hash_password, verify_password
from shared.backend.utils import new_id, now_iso

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear app FastAPI
app = FastAPI(
    title="NexoPro Platform API",
    description="ERP multi-sector: core de facturación + módulos sectoriales",
    version="2.0.0"
)

# CORS - Configurar en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers del CORE
app.include_router(contactos.router)
app.include_router(auth.router)
app.include_router(auth.licencias_router)

# TODO: Registrar routers sectoriales dinámicamente según licencia
# SECTOR_ROUTERS = {
#     "taller": [taller_vehiculos, taller_ordenes, ...],
#     "hosteleria": [hosteleria_mesas, ...],
# }


@app.get("/api/health")
async def health_check():
    """Endpoint de health check para monitoreo."""
    return {"status": "ok", "service": "nexopro-platform"}


@app.on_event("startup")
async def startup_seed():
    """Inicialización: índices, admin por defecto, licencia demo."""
    # Crear índices
    try:
        await db.users.create_index("email", unique=True)
        await db.licencias.create_index("license_key", unique=True)
        await db.contactos.create_index("id", unique=True)
        logger.info("Índices de MongoDB creados")
    except Exception as e:
        logger.warning(f"Índices ya existen o error: {e}")

    # Admin por defecto (SOLO si no existe)
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@nexopro.com").lower()
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_password:
        # Generar password aleatorio si no está configurado
        import secrets
        admin_password = secrets.token_urlsafe(16)
        logger.warning(f"ADMIN_PASSWORD no configurado. Password generado: {admin_password}")

    existing = await db.users.find_one({"email": admin_email})
    if existing is None:
        await db.users.insert_one({
            "id": new_id(),
            "email": admin_email,
            "password_hash": hash_password(admin_password),
            "name": "Administrador",
            "role": "admin",
            "created_at": now_iso(),
        })
        logger.info(f"Admin creado: {admin_email}")
    elif not verify_password(admin_password, existing["password_hash"]):
        # Actualizar password si cambió en .env
        await db.users.update_one(
            {"email": admin_email},
            {"$set": {"password_hash": hash_password(admin_password)}}
        )
        logger.info("Password de admin actualizado")

    # Licencia demo
    demo_key = os.environ.get("DEMO_LICENSE_KEY", "NEXO-DEMO-0001")
    if not await db.licencias.find_one({"license_key": demo_key}):
        await db.licencias.insert_one({
            "id": new_id(),
            "license_key": demo_key,
            "empresa": "Empresa Demo SL",
            "email": "demo@empresa.es",
            "telefono": "",
            "precio_mensual": 29,
            "estado": "activa",
            "sector": "taller",
            "modulos": ["taller"],
            "notas": "Licencia de demostración",
            "created_at": now_iso(),
        })
        logger.info(f"Licencia demo creada: {demo_key}")


@app.on_event("shutdown")
async def shutdown_db_client():
    """Cierra conexiones al apagar."""
    from core.backend.dependencies.database import client
    client.close()
    logger.info("Conexión a MongoDB cerrada")
