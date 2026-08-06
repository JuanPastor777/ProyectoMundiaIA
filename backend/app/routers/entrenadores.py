from fastapi import APIRouter
from app.schemas.catalogos import Entrenador, EntrenadorCreate, EntrenadorUpdate
from app.models import tablas
from app.services import crud

router = APIRouter(prefix="/api/entrenadores", tags=["Entrenadores"])


@router.get("", response_model=list[Entrenador])
def listar_entrenadores():
    return crud.listar(tablas.ENTRENADORES, orden="apellido")


@router.post("", response_model=Entrenador, status_code=201)
def crear_entrenador(datos: EntrenadorCreate):
    return crud.crear(tablas.ENTRENADORES, datos.model_dump())


@router.get("/{id}", response_model=Entrenador)
def obtener_entrenador(id: str):
    return crud.obtener_uno(tablas.ENTRENADORES, id)


@router.put("/{id}", response_model=Entrenador)
def editar_entrenador(id: str, datos: EntrenadorUpdate):
    return crud.actualizar(tablas.ENTRENADORES, id, datos.model_dump())


@router.delete("/{id}")
def eliminar_entrenador(id: str):
    return crud.eliminar(tablas.ENTRENADORES, id)
