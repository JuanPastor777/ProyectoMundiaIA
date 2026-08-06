from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date


# ---------- Selección ----------
class SeleccionBase(BaseModel):
    nombre: str
    codigo: str = Field(max_length=3)
    confederacion_id: UUID
    grupo_id: Optional[UUID] = None
    entrenador_id: Optional[UUID] = None


class SeleccionCreate(SeleccionBase):
    pass


class SeleccionUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    confederacion_id: Optional[UUID] = None
    grupo_id: Optional[UUID] = None
    entrenador_id: Optional[UUID] = None


class Seleccion(SeleccionBase):
    id: UUID


# ---------- Jugador ----------
POSICIONES_VALIDAS = ("PORTERO", "DEFENSA", "MEDIOCAMPISTA", "DELANTERO")


class JugadorBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    nacionalidad: Optional[str] = None
    posicion: str = Field(description="PORTERO | DEFENSA | MEDIOCAMPISTA | DELANTERO")
    numero_camiseta: int = Field(ge=1, le=99)
    seleccion_id: UUID


class JugadorCreate(JugadorBase):
    pass


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    posicion: Optional[str] = None
    numero_camiseta: Optional[int] = None
    seleccion_id: Optional[UUID] = None


class Jugador(JugadorBase):
    id: UUID
