"""Utilidades compartidas entre todos los módulos."""
import uuid
from datetime import datetime, timezone


def new_id() -> str:
    """Genera un UUID v4 como string."""
    return str(uuid.uuid4())


def now_iso() -> str:
    """Devuelve la fecha/hora actual en formato ISO 8601 UTC."""
    return datetime.now(timezone.utc).isoformat()
