from fastapi import APIRouter, Query
from app.schemas.catalogos import Ciudad, CiudadCreate, Estadio, EstadioCreate, EstadioUpdate
from app.models import tablas
from app.services import crud
from app.database import execute_query


router = APIRouter(tags=["Ciudades y Estadios"])


# ---------- Ciudades ----------

@router.get("/api/ciudades", response_model=list[Ciudad])
def listar_ciudades():
    return crud.listar(tablas.CIUDADES, orden="nombre")


@router.post("/api/ciudades", response_model=Ciudad, status_code=201)
def crear_ciudad(datos: CiudadCreate):
    return crud.crear(tablas.CIUDADES, datos.model_dump())


@router.delete("/api/ciudades/{id}")
def eliminar_ciudad(id: str):
    return crud.eliminar(tablas.CIUDADES, id)


# ---------- Estadios ----------

@router.get("/api/estadios", response_model=list[Estadio])
def listar_estadios():
    return crud.listar(tablas.ESTADIOS, orden="nombre")


@router.post("/api/estadios", response_model=Estadio, status_code=201)
def crear_estadio(datos: EstadioCreate):
    return crud.crear(
        tablas.ESTADIOS,
        datos.model_dump(mode="json")
    )


@router.get("/api/estadios/{id}", response_model=Estadio)
def obtener_estadio(id: str):
    return crud.obtener_uno(tablas.ESTADIOS, id)


@router.put("/api/estadios/{id}", response_model=Estadio)
def editar_estadio(id: str, datos: EstadioUpdate):
    return crud.actualizar(
        tablas.ESTADIOS,
        id,
        datos.model_dump(mode="json")
    )


@router.delete("/api/estadios/{id}")
def eliminar_estadio(id: str):
    return crud.eliminar(tablas.ESTADIOS, id)


@router.get("/api/estadios/disponibilidad")
def disponibilidad_estadios(
    fecha: str = Query(...),
    hora: str = Query(...)
):
    """
    Devuelve qué estadios están libres para una fecha y hora.
    """

    # Todos los estadios
    todos = crud.listar(tablas.ESTADIOS)

    # Buscar estadios ocupados
    ocupados = execute_query(
        """
        SELECT estadio_id
        FROM mundial.partidos
        WHERE fecha = %s
          AND hora = %s
          AND estado <> %s
        """,
        (fecha, hora, "CANCELADO")
    )

    ids_ocupados = {
        str(p["estadio_id"])
        for p in ocupados
    }

    disponibles = [
        e for e in todos
        if str(e["id"]) not in ids_ocupados
        and e["disponible"]
    ]

    ocupados_estadios = [
        e for e in todos
        if str(e["id"]) in ids_ocupados
    ]

    return {
        "fecha": fecha,
        "hora": hora,
        "estadios_disponibles": disponibles,
        "estadios_ocupados": ocupados_estadios,
    }