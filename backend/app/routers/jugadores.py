from fastapi import APIRouter
from app.schemas.selecciones import Jugador, JugadorCreate, JugadorUpdate
from app.models import tablas
from app.services import crud

router = APIRouter(prefix="/api/jugadores", tags=["Jugadores"])


@router.get("", response_model=list[Jugador])
def listar_jugadores():
    return crud.listar(tablas.JUGADORES, orden="apellido")


@router.post("", response_model=Jugador, status_code=201)
def crear_jugador(datos: JugadorCreate):
    return crud.crear(tablas.JUGADORES, datos.model_dump(mode="json"))


@router.get("/{id}", response_model=Jugador)
def obtener_jugador(id: str):
    return crud.obtener_uno(tablas.JUGADORES, id)


@router.put("/{id}", response_model=Jugador)
def editar_jugador(id: str, datos: JugadorUpdate):
    return crud.actualizar(tablas.JUGADORES, id, datos.model_dump(mode="json"))


@router.delete("/{id}")
def eliminar_jugador(id: str):
    return crud.eliminar(tablas.JUGADORES, id)
