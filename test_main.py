import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_recurso_exito():
    """Prueba que el endpoint POST cree un ítem correctamente sin tokens (Código 201)"""
    payload = {
        "title": "Item de prueba pública",
        "description": "Verificando el correcto funcionamiento del POST público",
        "priority": "alta",
        "completed": False
    }
    
    response = client.post("/items", json=payload)
    
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["codigo"] == 201
    assert json_data["estado"] == "exito"
    assert json_data["datos"]["title"] == "Item de prueba pública"

def test_crear_recurso_error_400_datos_invalidos():
    """Prueba que el endpoint POST devuelva un error si enviamos datos incompletos (Código 400)"""
    payload = {
        "title": "Item incompleto",
        "description": "Falta la prioridad"
    }
    
    response = client.post("/items", json=payload)
    
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["codigo"] == 400
    assert json_data["estado"] == "error"
    assert "Datos de entrada inválidos" in json_data["mensaje"]
