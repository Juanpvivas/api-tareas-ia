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
def listar(hecha: bool | None = None) -> list[Tarea]:
    tareas_listadas = list(tareas.values())
    if hecha is not None:
        tareas_listadas = [
            tarea for tarea in tareas_listadas if tarea.hecha == hecha
        ]
    return tareas_listadas

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

@app.delete("/tareas/{id}", status_code=204)
def eliminar(id: int) -> None:
    if id not in tareas:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del tareas[id]

@app.post("/tareas", status_code=201)
def crear(datos: TareaNueva) -> Tarea:
    global siguiente_id
    tarea = Tarea(id=siguiente_id, **datos.model_dump())
    tareas[tarea.id] = tarea
    siguiente_id += 1
    return tarea