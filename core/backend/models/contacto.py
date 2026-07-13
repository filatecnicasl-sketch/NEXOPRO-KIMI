"""Modelos para Clientes y Proveedores."""
from typing import Literal
from pydantic import BaseModel, Field
from .base import BaseDocument
from shared.backend.utils import new_id, now_iso


class Contacto(BaseDocument):
    """Cliente o Proveedor del sistema."""
    tipo: Literal['cliente', 'proveedor']
    nombre: str
    nif: str = ""
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    ciudad: str = ""
    codigo_postal: str = ""
    pais: str = "España"
    iban: str = ""
    banco: str = ""
    swift: str = ""
    direccion_entrega: str = ""
    ciudad_entrega: str = ""
    cp_entrega: str = ""
    es_publica: bool = False
    dir3_oficina_contable: str = ""
    dir3_organo_gestor: str = ""
    dir3_unidad_tramitadora: str = ""
    notas: str = ""


class ContactoInput(BaseModel):
    """Input para crear/actualizar un contacto."""
    tipo: Literal['cliente', 'proveedor']
    nombre: str
    nif: str = ""
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    ciudad: str = ""
    codigo_postal: str = ""
    pais: str = "España"
    iban: str = ""
    banco: str = ""
    swift: str = ""
    direccion_entrega: str = ""
    ciudad_entrega: str = ""
    cp_entrega: str = ""
    es_publica: bool = False
    dir3_oficina_contable: str = ""
    dir3_organo_gestor: str = ""
    dir3_unidad_tramitadora: str = ""
    notas: str = ""
