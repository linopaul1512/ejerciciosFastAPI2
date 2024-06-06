from typing import Union, List, Set
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Set, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

listaestudiantes = []


class Contenido(BaseModel):
    nombre: str
    decripcion: str
   
  
class Materia(BaseModel):
    id: int
    nombre: str
    nivel: str
    unidades_credito: int
    precio: float
    descripcion: str
    contenidos: Union[List[Contenido], None] = None

class Estudiante(BaseModel):
    id: int
    nombre: str
    apellido: str
    fecha_nacimiento: datetime
    telefono: str
    direcccion: str
    materias: List[Materia]



@app.get("/estudiantes", response_model=List[Estudiante])
def get_estudiantes() -> List[Estudiante]:
    return listaestudiantes

@app.post("/estudiantes/create", response_model=Estudiante)
def crear_estudiantes(estudiante: Estudiante):
    if any(m.id == estudiante.id for m in listaestudiantes):
        raise HTTPException(status_code=400, detail="Estudiante con este ID ya existe")
    listaestudiantes.append(estudiante)
    return estudiante

@app.get("/estudiantes/{id}", response_model=Estudiante)
def get_estudiante(id: int):
    estudiante = next((m for m in listaestudiantes if m.id == id), None)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrada")
    return estudiante

@app.get("/estudiantes/materias/{id}")
def get_record_academico(id: int):
    estudiante = next((m for m in listaestudiantes if m.id == id), None)
    if estudiante is None:
        raise HTTPException(status_code=404, detail="materias no encontrada")
    return estudiante.materias

@app.put("/estudiantes/{id}", response_model=Estudiante)
def update_estudiante(id: int, estudiante: Estudiante):
    index = next((i for i, m in enumerate(listaestudiantes) if m.id == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrada")
    listaestudiantes[index] = estudiante
    return estudiante

@app.delete("/estudiantes/{id}")
def delete_estudiante(id: int):
    index = next((i for i, m in enumerate(listaestudiantes) if m.id == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrada")
    del listaestudiantes[index]
    return {"mensaje": "Estudiante eliminada exitosamente."}

