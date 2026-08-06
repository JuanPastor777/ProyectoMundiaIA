from fastapi import APIRouter
from app.schemas.partidos import (
    Partido, PartidoCreate, PartidoUpdate, ResultadoInput, Incidencia, IncidenciaCreate,
)
from app.models import tablas
from app.services import crud
from app.services import partidos_service

router = APIRouter(prefix="/api/partidos", tags=["Partidos"])


@router.get("", response_model=list[Partido])
def listar_partidos():
    return crud.listar(tablas.PARTIDOS, orden="fecha")


@router.post("", response_model=Partido, status_code=201)
def programar_partido(datos: PartidoCreate):
    # Regla de negocio 2: validar que el estadio esté libre (además del UNIQUE en BD)
    partidos_service.validar_estadio_disponible(
        str(datos.estadio_id), datos.fecha.isoformat(), datos.hora.isoformat()
    )
    return crud.crear(tablas.PARTIDOS, datos.model_dump(mode="json"))


@router.get("/{id}", response_model=Partido)
def obtener_partido(id: str):
    return crud.obtener_uno(tablas.PARTIDOS, id)


@router.put("/{id}", response_model=Partido)
def editar_partido(id: str, datos: PartidoUpdate):
    if datos.estadio_id and datos.fecha and datos.hora:
        partidos_service.validar_estadio_disponible(
            str(datos.estadio_id), datos.fecha.isoformat(), datos.hora.isoformat(), partido_id_excluir=id
        )
    return crud.actualizar(tablas.PARTIDOS, id, datos.model_dump(mode="json"))


@router.post("/{id}/resultado", response_model=Partido)
def registrar_resultado(id: str, datos: ResultadoInput):
    """
    Registra el marcador final del partido y actualiza automáticamente
    la tabla de posiciones (estadisticas_seleccion). Acepta 0-0 (caso límite).
    """
    return partidos_service.registrar_resultado(id, datos.goles_local, datos.goles_visitante)


@router.post("/{id}/incidencias", response_model=Incidencia, status_code=201)
def registrar_incidencia(id: str, datos: IncidenciaCreate):
    payload = datos.model_dump(mode="json")
    payload["partido_id"] = id
    return crud.crear(tablas.INCIDENCIAS, payload)


@router.get("/{id}/incidencias", response_model=list[Incidencia])
def listar_incidencias_partido(id: str):
    return crud.listar(tablas.INCIDENCIAS, filtros={"partido_id": id})
