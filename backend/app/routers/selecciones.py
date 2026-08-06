from fastapi import APIRouter
from app.schemas.selecciones import Seleccion, SeleccionCreate, SeleccionUpdate
from app.models import tablas
from app.services import crud

router = APIRouter(prefix="/api/selecciones", tags=["Selecciones"])


@router.get("", response_model=list[Seleccion])
def listar_selecciones():
    return crud.listar(tablas.SELECCIONES, orden="nombre")


@router.post("", response_model=Seleccion, status_code=201)
def crear_seleccion(datos: SeleccionCreate):
    return crud.crear(tablas.SELECCIONES, datos.model_dump(mode="json"))


@router.get("/{id}", response_model=Seleccion)
def obtener_seleccion(id: str):
    return crud.obtener_uno(tablas.SELECCIONES, id)


@router.put("/{id}", response_model=Seleccion)
def editar_seleccion(id: str, datos: SeleccionUpdate):
    return crud.actualizar(tablas.SELECCIONES, id, datos.model_dump(mode="json"))


@router.delete("/{id}")
def eliminar_seleccion(id: str):
    return crud.eliminar(tablas.SELECCIONES, id)


@router.get("/{id}/jugadores")
def jugadores_de_seleccion(id: str):
    return crud.listar(tablas.JUGADORES, filtros={"seleccion_id": id})
