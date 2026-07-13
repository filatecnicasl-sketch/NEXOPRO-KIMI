"""Modelos para autenticación y licencias."""
from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseDocument
from shared.backend.utils import new_id, now_iso


class User(BaseDocument):
    """Usuario del sistema (admin o tenant)."""
    email: str
    password_hash: str
    name: str = ""
    role: str = "admin"  # admin, user


class Licencia(BaseDocument):
    """Licencia de un cliente/tenant."""
    license_key: str
    empresa: str
    email: str = ""
    telefono: str = ""
    precio_mensual: float = 29.0
    estado: str = "activa"  # activa, suspendida
    ultimo_pago: Optional[str] = None
    proximo_pago: Optional[str] = None
    sector: str = "taller"  # taller, hosteleria, retail, servicios
    modulos: list = Field(default_factory=list)
    notas: str = ""


class LoginInput(BaseModel):
    """Input para login."""
    email: str
    password: str
