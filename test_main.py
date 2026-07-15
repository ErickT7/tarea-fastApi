import pytest
from fastapi.testclient import TestClient
from main import app, TOKEN_SECRETO

# Inicializamos el cliente de pruebas nativo de FastAPI
client = TestClient(app)

def test_crear_recurso_exito():
    """Prueba que el endpoint POST cree un ítem correctamente si mandamos el Token y los datos válidos (Código 201)"""
    headers = {"Authorization": f"Bearer {TOKEN_SECRETO}"}
    payload = {
        "title": "Item de prueba unitaria",
        "description": "Verificando el correcto funcionamiento del POST",
        "priority": "alta",
        "completed": False
    }
    
    response = client.post("/items", json=payload, headers=headers)
    
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["codigo"] == 201
    assert json_data["estado"] == "exito"
    assert json_data["datos"]["title"] == "Item de prueba unitaria"

def test_crear_recurso_error_401_no_autorizado():
    """Prueba que el endpoint POST bloquee la creación si no enviamos la cabecera Token (Código 401)"""
    payload = {
        "title": "Item intruso",
        "description": "No tengo permisos",
        "priority": "baja"
    }
    
    response = client.post("/items", json=payload)
    
    assert response.status_code == 401
    json_data = response.json()
    assert json_data["codigo"] == 401
    assert json_data["estado"] == "error"
    assert "Falta la cabecera de autenticación" in json_data["mensaje"]

def test_crear_recurso_error_400_datos_invalidos():
    """Prueba que el endpoint POST devuelva un error si enviamos datos incompletos (Código 400)"""
    headers = {"Authorization": f"Bearer {TOKEN_SECRETO}"}
    # Payload inválido: le falta el campo obligatorio 'priority'
    payload = {
        "title": "Item incompleto",
        "description": "Falta la prioridad"
    }
    
    response = client.post("/items", json=payload, headers=headers)
    
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["codigo"] == 400
    assert json_data["estado"] == "error"
    assert "Datos de entrada inválidos" in json_data["mensaje"]
