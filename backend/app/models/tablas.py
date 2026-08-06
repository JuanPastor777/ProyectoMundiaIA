"""
Como el acceso a datos se hace vía el cliente de Supabase (PostgREST) y no
mediante un ORM, este módulo centraliza los nombres de las tablas para
evitar strings "mágicos" repetidos en los routers.
"""

CONFEDERACIONES = "confederaciones"
GRUPOS = "grupos"
CIUDADES = "ciudades"
ESTADIOS = "estadios"
ENTRENADORES = "entrenadores"
SELECCIONES = "selecciones"
JUGADORES = "jugadores"
PARTIDOS = "partidos"
INCIDENCIAS = "incidencias"
ESTADISTICAS_JUGADOR = "estadisticas_jugador"
ESTADISTICAS_SELECCION = "estadisticas_seleccion"
