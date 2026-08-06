from fastapi import APIRouter
from app.schemas.catalogos import Confederacion, ConfederacionCreate, Grupo, GrupoCreate
from app.models import tablas
from app.services import crud

router = APIRouter(tags=["Confederaciones y Grupos"])


# ---------- Confederaciones ----------
@router.get("/api/confederaciones", response_model=list[Confederacion])
def listar_confederaciones():
    return crud.listar(tablas.CONFEDERACIONES, orden="nombre")


@router.post("/api/confederaciones", response_model=Confederacion, status_code=201)
def crear_confederacion(datos: ConfederacionCreate):
    return crud.crear(tablas.CONFEDERACIONES, datos.model_dump())


@router.get("/api/confederaciones/{id}", response_model=Confederacion)
def obtener_confederacion(id: str):
    return crud.obtener_uno(tablas.CONFEDERACIONES, id)


@router.delete("/api/confederaciones/{id}")
def eliminar_confederacion(id: str):
    return crud.eliminar(tablas.CONFEDERACIONES, id)


# ---------- Grupos ----------
@router.get("/api/grupos", response_model=list[Grupo])
def listar_grupos():
    return crud.listar(tablas.GRUPOS, orden="nombre")


@router.post("/api/grupos", response_model=Grupo, status_code=201)
def crear_grupo(datos: GrupoCreate):
    return crud.crear(tablas.GRUPOS, datos.model_dump())


@router.get("/api/grupos/{id}", response_model=Grupo)
def obtener_grupo(id: str):
    return crud.obtener_uno(tablas.GRUPOS, id)


@router.get("/api/grupos/{id}/selecciones")
def selecciones_del_grupo(id: str):
    """Selecciones que pertenecen a un grupo, útil para la tabla de posiciones."""
    return crud.listar(tablas.SELECCIONES, filtros={"grupo_id": id})


@router.get("/api/grupos/{id}/partidos")
def partidos_del_grupo(id: str):
    return crud.listar(tablas.PARTIDOS, filtros={"grupo_id": id}, orden="fecha")


@router.delete("/api/grupos/{id}")
def eliminar_grupo(id: str):
    return crud.eliminar(tablas.GRUPOS, id)
