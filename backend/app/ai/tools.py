"""
Tools del agente de IA.

REGLA DE SEGURIDAD:
Todas las funciones de este archivo son únicamente de LECTURA.
No realizan INSERT, UPDATE ni DELETE.
"""

from app.database import execute_query


# ---------------------------------------------------------------------
# TOOL 1 — Partidos
# ---------------------------------------------------------------------
def consultar_partidos(
    fecha: str | None = None,
    seleccion: str | None = None,
    estado: str | None = None
) -> dict:

    sql = """
        SELECT
            p.id,
            p.fecha,
            p.hora,
            p.fase,
            p.estado,
            p.goles_local,
            p.goles_visitante,

            e.nombre AS estadio,

            sl.nombre AS seleccion_local,
            sl.codigo AS codigo_local,

            sv.nombre AS seleccion_visitante,
            sv.codigo AS codigo_visitante

        FROM mundial.partidos p

        LEFT JOIN mundial.estadios e
            ON e.id = p.estadio_id

        LEFT JOIN mundial.selecciones sl
            ON sl.id = p.seleccion_local_id

        LEFT JOIN mundial.selecciones sv
            ON sv.id = p.seleccion_visitante_id

        WHERE 1 = 1
    """

    parametros = []

    if fecha:
        sql += " AND p.fecha = %s"
        parametros.append(fecha)

    if estado:
        sql += " AND p.estado = %s"
        parametros.append(estado)

    sql += " ORDER BY p.fecha, p.hora"

    partidos = execute_query(sql, parametros)

    if seleccion:
        s = seleccion.strip().lower()

        partidos = [
            p for p in partidos
            if (
                s in (p.get("seleccion_local") or "").lower()
                or s in (p.get("seleccion_visitante") or "").lower()
                or s == (p.get("codigo_local") or "").lower()
                or s == (p.get("codigo_visitante") or "").lower()
            )
        ]

    if not partidos:
        return {
            "encontrado": False,
            "mensaje": "No se encontraron partidos con esos criterios."
        }

    return {
        "encontrado": True,
        "partidos": partidos
    }


# ---------------------------------------------------------------------
# TOOL 2 — Selección
# ---------------------------------------------------------------------
def consultar_seleccion(nombre_o_codigo: str) -> dict:

    sql = """
        SELECT
            s.id,
            s.nombre,
            s.codigo,

            c.nombre AS confederacion,
            g.nombre AS grupo,

            CONCAT(e.nombre, ' ', e.apellido) AS entrenador

        FROM mundial.selecciones s

        LEFT JOIN mundial.confederaciones c
            ON c.id = s.confederacion_id

        LEFT JOIN mundial.grupos g
            ON g.id = s.grupo_id

        LEFT JOIN mundial.entrenadores e
            ON e.id = s.entrenador_id

        WHERE LOWER(s.nombre) = LOWER(%s)
           OR LOWER(s.codigo) = LOWER(%s)

        LIMIT 1
    """

    resultado = execute_query(
        sql,
        [nombre_o_codigo, nombre_o_codigo]
    )

    if not resultado:
        return {
            "encontrado": False,
            "mensaje": f"No existe información registrada para '{nombre_o_codigo}'."
        }

    seleccion = resultado[0]

    sql_jugadores = """
        SELECT
            nombre,
            apellido,
            posicion,
            numero_camiseta
        FROM mundial.jugadores
        WHERE seleccion_id = %s
        ORDER BY numero_camiseta
    """

    jugadores = execute_query(
        sql_jugadores,
        [seleccion["id"]]
    )

    seleccion["jugadores"] = jugadores

    return {
        "encontrado": True,
        "seleccion": seleccion
    }


# ---------------------------------------------------------------------
# TOOL 3 — Goleadores
# ---------------------------------------------------------------------
def consultar_goleadores(limite: int = 10) -> dict:

    sql = """
        SELECT
            j.nombre,
            j.apellido,
            SUM(e.goles) AS goles

        FROM mundial.estadisticas_jugador e

        INNER JOIN mundial.jugadores j
            ON j.id = e.jugador_id

        GROUP BY
            j.id,
            j.nombre,
            j.apellido

        ORDER BY SUM(e.goles) DESC

        LIMIT %s
    """

    goleadores = execute_query(sql, [limite])

    if not goleadores:
        return {
            "encontrado": False,
            "mensaje": "Aún no hay goles registrados en el torneo."
        }

    resultado = []

    for jugador in goleadores:
        resultado.append({
            "jugador": f"{jugador['nombre']} {jugador['apellido']}",
            "goles": jugador["goles"]
        })

    return {
        "encontrado": True,
        "goleadores": resultado
    }


# ---------------------------------------------------------------------
# TOOL 4 — Disponibilidad de estadios
# ---------------------------------------------------------------------
def consultar_disponibilidad_estadio(
    fecha: str,
    hora: str
) -> dict:

    sql = """
        SELECT *
        FROM mundial.estadios
        ORDER BY nombre
    """

    todos = execute_query(sql)

    sql_ocupados = """
        SELECT estadio_id
        FROM mundial.partidos
        WHERE fecha = %s
          AND hora = %s
          AND estado <> 'CANCELADO'
    """

    ocupados = execute_query(
        sql_ocupados,
        [fecha, hora]
    )

    ids_ocupados = {
        p["estadio_id"]
        for p in ocupados
    }

    disponibles = [
        e["nombre"]
        for e in todos
        if e["id"] not in ids_ocupados
        and e["disponible"]
    ]

    return {
        "fecha": fecha,
        "hora": hora,
        "estadios_disponibles": disponibles
    }


# ---------------------------------------------------------------------
# TOOL 5 — Reporte de grupo
# ---------------------------------------------------------------------
def generar_reporte_grupo(nombre_grupo: str) -> dict:

    sql_grupo = """
        SELECT id, nombre
        FROM mundial.grupos
        WHERE LOWER(nombre) = LOWER(%s)
        LIMIT 1
    """

    grupos = execute_query(
        sql_grupo,
        [nombre_grupo]
    )

    if not grupos:
        return {
            "encontrado": False,
            "mensaje": f"No existe el grupo '{nombre_grupo}'."
        }

    grupo = grupos[0]

    sql_selecciones = """
        SELECT
            id,
            nombre,
            codigo
        FROM mundial.selecciones
        WHERE grupo_id = %s
        ORDER BY nombre
    """

    selecciones = execute_query(
        sql_selecciones,
        [grupo["id"]]
    )

    posiciones = []

    for seleccion in selecciones:

        sql_estadistica = """
            SELECT
                partidos_jugados,
                puntos,
                goles_favor,
                goles_contra
            FROM mundial.estadisticas_seleccion
            WHERE seleccion_id = %s
            LIMIT 1
        """

        estadisticas = execute_query(
            sql_estadistica,
            [seleccion["id"]]
        )

        if estadisticas:

            e = estadisticas[0]

            posiciones.append({
                "seleccion": seleccion["nombre"],
                "pj": e["partidos_jugados"],
                "pts": e["puntos"],
                "gf": e["goles_favor"],
                "gc": e["goles_contra"]
            })

        else:

            posiciones.append({
                "seleccion": seleccion["nombre"],
                "pj": 0,
                "pts": 0,
                "gf": 0,
                "gc": 0
            })

    posiciones.sort(
        key=lambda x: (
            -x["pts"],
            -(x["gf"] - x["gc"]),
            -x["gf"]
        )
    )

    sql_partidos = """
        SELECT
            p.fecha,
            p.hora,
            p.estado,
            p.goles_local,
            p.goles_visitante,

            sl.nombre AS seleccion_local,
            sv.nombre AS seleccion_visitante

        FROM mundial.partidos p

        LEFT JOIN mundial.selecciones sl
            ON sl.id = p.seleccion_local_id

        LEFT JOIN mundial.selecciones sv
            ON sv.id = p.seleccion_visitante_id

        WHERE p.grupo_id = %s

        ORDER BY p.fecha, p.hora
    """

    partidos = execute_query(
        sql_partidos,
        [grupo["id"]]
    )

    return {
        "encontrado": True,
        "grupo": grupo["nombre"],
        "posiciones": posiciones,
        "partidos": partidos
    }


# ---------------------------------------------------------------------
# TOOL 6 — Goles totales
# ---------------------------------------------------------------------
def consultar_goles_totales_torneo() -> dict:

    sql = """
        SELECT
            COALESCE(
                SUM(
                    COALESCE(goles_local, 0)
                    +
                    COALESCE(goles_visitante, 0)
                ),
                0
            ) AS total_goles,

            COUNT(*) AS partidos_finalizados

        FROM mundial.partidos

        WHERE estado = 'FINALIZADO'
    """

    resultado = execute_query(sql)

    if not resultado:
        return {
            "total_goles": 0,
            "partidos_finalizados": 0
        }

    return {
        "total_goles": resultado[0]["total_goles"],
        "partidos_finalizados": resultado[0]["partidos_finalizados"]
    }


# ---------------------------------------------------------------------
# DEFINICIÓN DE TOOLS PARA OPENAI
# ---------------------------------------------------------------------

TOOLS_OPENAI = [

    {
        "type": "function",
        "function": {
            "name": "consultar_partidos",
            "description": "Consulta partidos del torneo por fecha, selección o estado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha": {
                        "type": "string",
                        "description": "Fecha en formato YYYY-MM-DD"
                    },
                    "seleccion": {
                        "type": "string",
                        "description": "Nombre o código de una selección"
                    },
                    "estado": {
                        "type": "string",
                        "enum": [
                            "PROGRAMADO",
                            "EN_CURSO",
                            "FINALIZADO",
                            "CANCELADO"
                        ]
                    }
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "consultar_seleccion",
            "description": "Consulta información de una selección, entrenador, grupo, confederación y jugadores.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_o_codigo": {
                        "type": "string",
                        "description": "Nombre o código de la selección"
                    }
                },
                "required": ["nombre_o_codigo"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "consultar_goleadores",
            "description": "Devuelve los jugadores con más goles en el torneo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limite": {
                        "type": "integer",
                        "description": "Cantidad de jugadores a mostrar"
                    }
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "consultar_disponibilidad_estadio",
            "description": "Consulta qué estadios están disponibles en una fecha y hora.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha": {
                        "type": "string",
                        "description": "Fecha YYYY-MM-DD"
                    },
                    "hora": {
                        "type": "string",
                        "description": "Hora HH:MM"
                    }
                },
                "required": ["fecha", "hora"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "generar_reporte_grupo",
            "description": "Genera la tabla de posiciones y partidos de un grupo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_grupo": {
                        "type": "string",
                        "description": "Nombre del grupo, por ejemplo Grupo A"
                    }
                },
                "required": ["nombre_grupo"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "consultar_goles_totales_torneo",
            "description": "Devuelve el total de goles del torneo.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# ---------------------------------------------------------------------
# MAPEO DE FUNCIONES
# ---------------------------------------------------------------------

FUNCIONES_DISPONIBLES = {
    "consultar_partidos": consultar_partidos,
    "consultar_seleccion": consultar_seleccion,
    "consultar_goleadores": consultar_goleadores,
    "consultar_disponibilidad_estadio": consultar_disponibilidad_estadio,
    "generar_reporte_grupo": generar_reporte_grupo,
    "consultar_goles_totales_torneo": consultar_goles_totales_torneo,
}