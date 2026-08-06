from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import UUID
from datetime import date, time

ESTADOS_VALIDOS = ("PROGRAMADO", "EN_CURSO", "FINALIZADO", "CANCELADO")
FASES_VALIDAS = ("GRUPOS", "OCTAVOS", "CUARTOS", "SEMIFINAL", "FINAL", "TERCER_PUESTO")
TIPOS_INCIDENCIA = ("GOL", "TARJETA_AMARILLA", "TARJETA_ROJA", "SUSTITUCION",
                     "LESION", "PENAL", "AUTOGOL")


class PartidoBase(BaseModel):
    fecha: date
    hora: time
    estadio_id: UUID
    grupo_id: Optional[UUID] = None
    fase: str = "GRUPOS"
    seleccion_local_id: UUID
    seleccion_visitante_id: UUID

    @model_validator(mode="after")
    def equipos_distintos(self):
        if self.seleccion_local_id == self.seleccion_visitante_id:
            raise ValueError("La selección local y visitante no pueden ser la misma.")
        return self


class PartidoCreate(PartidoBase):
    pass


class PartidoUpdate(BaseModel):
    fecha: Optional[date] = None
    hora: Optional[time] = None
    estadio_id: Optional[UUID] = None
    grupo_id: Optional[UUID] = None
    fase: Optional[str] = None
    seleccion_local_id: Optional[UUID] = None
    seleccion_visitante_id: Optional[UUID] = None
    estado: Optional[str] = None


class Partido(PartidoBase):
    id: UUID
    estado: str
    goles_local: Optional[int] = None
    goles_visitante: Optional[int] = None


class ResultadoInput(BaseModel):
    goles_local: int = Field(ge=0)
    goles_visitante: int = Field(ge=0)


class IncidenciaBase(BaseModel):
    jugador_id: Optional[UUID] = None
    minuto: int = Field(ge=0, le=130)
    tipo: str = Field(description="GOL | TARJETA_AMARILLA | TARJETA_ROJA | SUSTITUCION | LESION | PENAL | AUTOGOL")
    descripcion: Optional[str] = None


class IncidenciaCreate(IncidenciaBase):
    pass


class Incidencia(IncidenciaBase):
    id: UUID
    partido_id: UUID
