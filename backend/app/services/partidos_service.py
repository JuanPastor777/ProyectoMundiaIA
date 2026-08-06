"""
Lógica de negocio relacionada con partidos:

- Validar que el estadio esté libre en esa fecha/hora antes de programar.
- Al registrar un resultado, actualizar la tabla de posiciones
  (estadisticas_seleccion) y dejar el partido como FINALIZADO.

La aplicación utiliza conexión directa a PostgreSQL.
"""

from fastapi import HTTPException
from app.database import execute_query
from app.models import tablas


def validar_estadio_disponible(
    estadio_id: str,
    fecha: str,
    hora: str,
    partido_id_excluir: str | None = None
):
    """
    No se puede programar dos partidos en el mismo estadio
    a la misma fecha y hora.
    """

    sql = f"""
        SELECT id
        FROM mundial.{tablas.PARTIDOS}
        WHERE estadio_id = %s
          AND fecha = %s
          AND hora = %s
          AND estado <> %s
    """

    parametros = (
        estadio_id,
        fecha,
        hora,
        "CANCELADO"
    )

    conflictos = execute_query(sql, parametros)

    if partido_id_excluir:
        conflictos = [
            p for p in conflictos
            if str(p["id"]) != str(partido_id_excluir)
        ]

    if conflictos:
        raise HTTPException(
            status_code=409,
            detail=(
                "El estadio seleccionado ya tiene un partido "
                "programado en esa fecha y hora."
            ),
        )


def _resultado_desde_perspectiva(
    goles_favor: int,
    goles_contra: int
) -> tuple[int, int, int, int]:
    """
    Devuelve:
    (victorias, empates, derrotas, puntos)
    """

    if goles_favor > goles_contra:
        return 1, 0, 0, 3

    if goles_favor == goles_contra:
        return 0, 1, 0, 1

    return 0, 0, 1, 0


def _sumar_estadistica_seleccion(
    seleccion_id: str,
    goles_favor: int,
    goles_contra: int
):
    """
    Actualiza las estadísticas de una selección
    después de registrar un partido.
    """

    victorias, empates, derrotas, puntos = (
        _resultado_desde_perspectiva(
            goles_favor,
            goles_contra
        )
    )

    sql_buscar = f"""
        SELECT *
        FROM mundial.{tablas.ESTADISTICAS_SELECCION}
        WHERE seleccion_id = %s
    """

    existente = execute_query(
        sql_buscar,
        (seleccion_id,)
    )

    if existente:

        actual = existente[0]

        nuevos = {
            "partidos_jugados": actual["partidos_jugados"] + 1,
            "victorias": actual["victorias"] + victorias,
            "empates": actual["empates"] + empates,
            "derrotas": actual["derrotas"] + derrotas,
            "goles_favor": actual["goles_favor"] + goles_favor,
            "goles_contra": actual["goles_contra"] + goles_contra,
            "puntos": actual["puntos"] + puntos,
        }

        sql_update = f"""
            UPDATE mundial.{tablas.ESTADISTICAS_SELECCION}
            SET
                partidos_jugados = %s,
                victorias = %s,
                empates = %s,
                derrotas = %s,
                goles_favor = %s,
                goles_contra = %s,
                puntos = %s
            WHERE seleccion_id = %s
        """

        execute_query(
            sql_update,
            (
                nuevos["partidos_jugados"],
                nuevos["victorias"],
                nuevos["empates"],
                nuevos["derrotas"],
                nuevos["goles_favor"],
                nuevos["goles_contra"],
                nuevos["puntos"],
                seleccion_id,
            )
        )

    else:

        sql_insert = f"""
            INSERT INTO mundial.{tablas.ESTADISTICAS_SELECCION}
            (
                seleccion_id,
                partidos_jugados,
                victorias,
                empates,
                derrotas,
                goles_favor,
                goles_contra,
                puntos
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        execute_query(
            sql_insert,
            (
                seleccion_id,
                1,
                victorias,
                empates,
                derrotas,
                goles_favor,
                goles_contra,
                puntos,
            )
        )


def registrar_resultado(
    partido_id: str,
    goles_local: int,
    goles_visitante: int
) -> dict:
    """
    Registra el resultado de un partido y actualiza
    las estadísticas de ambas selecciones.
    """

    sql_partido = f"""
        SELECT *
        FROM mundial.{tablas.PARTIDOS}
        WHERE id = %s
    """

    partidos = execute_query(
        sql_partido,
        (partido_id,)
    )

    if not partidos:
        raise HTTPException(
            status_code=404,
            detail="Partido no encontrado."
        )

    partido = partidos[0]

    if partido["estado"] == "FINALIZADO":
        raise HTTPException(
            status_code=400,
            detail="Este partido ya tiene un resultado registrado."
        )

    if partido["estado"] == "CANCELADO":
        raise HTTPException(
            status_code=400,
            detail=(
                "No se puede registrar resultado "
                "de un partido cancelado."
            )
        )

    # 0-0 es un resultado válido.
    sql_update = f"""
        UPDATE mundial.{tablas.PARTIDOS}
        SET
            goles_local = %s,
            goles_visitante = %s,
            estado = %s
        WHERE id = %s
        RETURNING *
    """

    resultado = execute_query(
        sql_update,
        (
            goles_local,
            goles_visitante,
            "FINALIZADO",
            partido_id,
        )
    )

    _sumar_estadistica_seleccion(
        partido["seleccion_local_id"],
        goles_local,
        goles_visitante
    )

    _sumar_estadistica_seleccion(
        partido["seleccion_visitante_id"],
        goles_visitante,
        goles_local
    )

    return resultado[0]