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

def test_filtrar_tareas_hechas():
    pendiente = cliente.post("/tareas", json={"titulo": "Tarea pendiente"}).json()
    hecha = cliente.post("/tareas", json={"titulo": "Tarea hecha"}).json()
    cliente.patch(f"/tareas/{hecha['id']}")

    respuesta = cliente.get("/tareas", params={"hecha": True})

    assert respuesta.status_code == 200
    tareas_hechas = respuesta.json()
    ids_hechas = [tarea["id"] for tarea in tareas_hechas]
    assert hecha["id"] in ids_hechas
    assert pendiente["id"] not in ids_hechas
    assert all(tarea["hecha"] is True for tarea in tareas_hechas)

def test_filtrar_tareas_pendientes():
    pendiente = cliente.post("/tareas", json={"titulo": "Otra pendiente"}).json()
    hecha = cliente.post("/tareas", json={"titulo": "Otra hecha"}).json()
    cliente.patch(f"/tareas/{hecha['id']}")

    respuesta = cliente.get("/tareas", params={"hecha": False})

    assert respuesta.status_code == 200
    tareas_pendientes = respuesta.json()
    ids_pendientes = [tarea["id"] for tarea in tareas_pendientes]
    assert pendiente["id"] in ids_pendientes
    assert hecha["id"] not in ids_pendientes
    assert all(tarea["hecha"] is False for tarea in tareas_pendientes)

def test_filtrar_tareas_con_estado_invalido_devuelve_422():
    respuesta = cliente.get("/tareas", params={"hecha": "invalido"})

    assert respuesta.status_code == 422

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

def test_marcar_tarea_como_hecha():
    creada = cliente.post("/tareas", json={"titulo": "Completar ejercicio"})
    id_tarea = creada.json()["id"]

    respuesta = cliente.patch(f"/tareas/{id_tarea}")

    assert respuesta.status_code == 200
    assert respuesta.json()["hecha"] is True
    assert cliente.get(f"/tareas/{id_tarea}").json()["hecha"] is True

def test_marcar_tarea_inexistente_devuelve_404():
    ids_existentes = [
        tarea["id"] for tarea in cliente.get("/tareas").json()
    ]
    id_inexistente = max(ids_existentes, default=0) + 1

    respuesta = cliente.patch(f"/tareas/{id_inexistente}")

    assert respuesta.status_code == 404

def test_eliminar_tarea_existente():
    creada = cliente.post("/tareas", json={"titulo": "Eliminar tarea"})
    id_tarea = creada.json()["id"]

    respuesta = cliente.delete(f"/tareas/{id_tarea}")

    assert respuesta.status_code == 204
    assert cliente.get(f"/tareas/{id_tarea}").status_code == 404

def test_eliminar_tarea_inexistente_devuelve_404():
    ids_existentes = [
        tarea["id"] for tarea in cliente.get("/tareas").json()
    ]
    id_inexistente = max(ids_existentes, default=0) + 1

    respuesta = cliente.delete(f"/tareas/{id_inexistente}")

    assert respuesta.status_code == 404