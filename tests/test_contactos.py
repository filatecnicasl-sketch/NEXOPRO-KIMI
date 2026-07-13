"""Tests para el módulo de contactos."""
import pytest
from httpx import AsyncClient
from core.backend.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_crear_contacto(client):
    response = await client.post("/api/contactos", json={
        "tipo": "cliente",
        "nombre": "Test Cliente SL",
        "nif": "B12345678",
        "email": "test@cliente.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Cliente SL"
    assert data["tipo"] == "cliente"
    assert "id" in data


@pytest.mark.asyncio
async def test_listar_contactos(client):
    response = await client.get("/api/contactos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
