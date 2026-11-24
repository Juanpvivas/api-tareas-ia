from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de tareas")

class TareaNueva(BaseModel):
    titulo: str
    hecha: bool = False

class Tarea(TareaNueva):
    id: int

tareas: dict[int, Tarea] = {}
siguiente_id = 1

@app.get("/tareas")
def listar() -> list[Tarea]:
    return list(tareas.values())

@app.get("/tareas/{id}")
def obtener(id: int) -> Tarea:
    if id not in tareas:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tareas[id]

@app.patch("/tareas/{id}")
def marcar_como_hecha(id: int) -> Tarea:
    if id not in tareas:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tareas[id].hecha = True
    return tareas[id]

@app.post("/tareas", status_code=201)
def crear(datos: TareaNueva) -> Tarea:
    global siguiente_id
    tarea = Tarea(id=siguiente_id, **datos.model_dump())
    tareas[tarea.id] = tarea
    siguiente_id += 1
    return tarea