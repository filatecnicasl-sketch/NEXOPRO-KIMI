"""Configuración de conexión a MongoDB."""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "nexopro")

# Cliente global
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


async def get_db():
    """Dependency para inyectar la base de datos en rutas."""
    return db
