from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Lista que almacena todas las materias
listamaterias = []

# Clase para manejar los datos de un profesor
class Profesor(BaseModel):
    id: int
    nombre: str
    apellido: str
    fecha_nacimiento: datetime
    fecha_inicio: datetime
    nivel: str
    años_experiencia: int

# Clase para manejar los datos de una materia
class Materia(BaseModel):
    id: int
    nombre: str
    contenido: str
    nivel: str
    costo: int
    carga_academica: str
    listaprofesores: List[Profesor] = []  # Lista de profesores asociados a la materia
    listaprerrequisitos: List[str] = []  # Lista de IDs de materias que son prerrequisitos

# Ruta para obtener todas las materias
@app.get("/materias", response_model=List[Materia])
def get_materias() -> List[Materia]:
    return listamaterias

# Ruta para crear una nueva materia
@app.post("/materias/", response_model=Materia)
def crear_materia(materia: Materia):
    if any(m.id == materia.id for m in listamaterias):
        raise HTTPException(status_code=400, detail="Materia con este ID ya existe")
    listamaterias.append(materia)
    return materia

# Ruta para obtener una materia por su ID
@app.get("/materias/{id}", response_model=Materia)
def get_materia(id: int):
    materia = next((m for m in listamaterias if m.id == id), None)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia

# Ruta para actualizar una materia existente
@app.put("/materias/{id}", response_model=Materia)
def update_materia(id: int, materia: Materia):
    index = next((i for i, m in enumerate(listamaterias) if m.id == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    listamaterias[index] = materia
    return materia

# Ruta para eliminar una materia por su ID
@app.delete("/materias/{id}")
def delete_materia(id: int):
    index = next((i for i, m in enumerate(listamaterias) if m.id == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    del listamaterias[index]
    return {"mensaje": "Materia eliminada exitosamente."}

