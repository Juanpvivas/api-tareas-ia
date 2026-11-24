from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)

def test_crear_y_listar():
    respuesta = cliente.post("/tareas", json={"titulo": "Estudiar FastAPI"})
    assert respuesta.status_code == 201
    tarea = respuesta.json()
    assert tarea["titulo"] == "Estudiar FastAPI"
    assert tarea["hecha"] is False
    
    lista = cliente.get("/tareas").json()
    assert tarea in lista

def test_obtener_tarea_existente():
    creada = cliente.post("/tareas", json={"titulo": "Practicar pruebas"})
    id_tarea = creada.json()["id"]

    respuesta = cliente.get(f"/tareas/{id_tarea}")

    assert respuesta.status_code == 200
    assert respuesta.json() == creada.json()

def test_obtener_tarea_inexistente_devuelve_404():
    ids_existentes = [
        tarea["id"] for tarea in cliente.get("/tareas").json()
    ]
    id_inexistente = max(ids_existentes, default=0) + 1

    respuesta = cliente.get(f"/tareas/{id_inexistente}")

    assert respuesta.status_code == 404