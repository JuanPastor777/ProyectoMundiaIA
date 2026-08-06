from fastapi import APIRouter
from app.models import tablas
from app.services import crud


router = APIRouter(tags=["Estadísticas y Dashboard"])


@router.get("/api/estadisticas")
def tabla_de_posiciones():
    """Tabla de posiciones ordenada por puntos, luego diferencia de goles."""
    datos = crud.listar(tablas.ESTADISTICAS_SELECCION)

    for fila in datos:
        fila["diferencia_goles"] = (
            fila["goles_favor"] - fila["goles_contra"]
        )

    datos.sort(
        key=lambda f: (
            -f["puntos"],
            -f["diferencia_goles"],
            -f["goles_favor"]
        )
    )

    return datos


@router.get("/api/estadisticas/jugadores")
def estadisticas_jugadores():
    return crud.listar(tablas.ESTADISTICAS_JUGADOR)


@router.get("/api/dashboard")
def resumen_dashboard():

    selecciones = crud.listar(tablas.SELECCIONES)
    jugadores = crud.listar(tablas.JUGADORES)
    partidos = crud.listar(tablas.PARTIDOS)
    estadios = crud.listar(tablas.ESTADIOS)

    programados = [
        p for p in partidos
        if p["estado"] == "PROGRAMADO"
    ]

    finalizados = [
        p for p in partidos
        if p["estado"] == "FINALIZADO"
    ]

    total_goles = sum(
        (p.get("goles_local") or 0)
        + (p.get("goles_visitante") or 0)
        for p in finalizados
    )

    proximos = sorted(
        programados,
        key=lambda p: (p["fecha"], p["hora"])
    )[:5]

    return {
        "total_selecciones": len(selecciones),
        "total_jugadores": len(jugadores),
        "partidos_programados": len(programados),
        "partidos_finalizados": len(finalizados),
        "estadios_disponibles": len(
            [e for e in estadios if e["disponible"]]
        ),
        "total_goles_torneo": total_goles,
        "proximos_partidos": proximos,
    }