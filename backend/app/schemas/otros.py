from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class EstadisticaSeleccion(BaseModel):
    seleccion_id: UUID
    partidos_jugados: int
    victorias: int
    empates: int
    derrotas: int
    goles_favor: int
    goles_contra: int
    puntos: int


class EstadisticaJugador(BaseModel):
    jugador_id: UUID
    partido_id: UUID
    goles: int
    asistencias: int
    tarjetas_amarillas: int
    tarjetas_rojas: int
    minutos_jugados: int


class ChatRequest(BaseModel):
    mensaje: str


class ChatResponse(BaseModel):
    respuesta: str
