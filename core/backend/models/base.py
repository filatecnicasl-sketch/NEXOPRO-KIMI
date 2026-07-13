"""Modelos base y utilidades para todos los modelos del core."""
from pydantic import BaseModel, Field
from shared.backend.utils import new_id, now_iso


class BaseDocument(BaseModel):
    """Modelo base para todos los documentos de MongoDB."""
    id: str = Field(default_factory=new_id)
    created_at: str = Field(default_factory=now_iso)
