from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# ---------- Confederación ----------
class ConfederacionBase(BaseModel):
    nombre: str
    codigo: str = Field(max_length=10)


class ConfederacionCreate(ConfederacionBase):
    pass


class Confederacion(ConfederacionBase):
    id: UUID


# ---------- Grupo ----------
class GrupoBase(BaseModel):
    nombre: str


class GrupoCreate(GrupoBase):
    pass


class Grupo(GrupoBase):
    id: UUID


# ---------- Ciudad ----------
class CiudadBase(BaseModel):
    nombre: str
    pais: str


class CiudadCreate(CiudadBase):
    pass


class Ciudad(CiudadBase):
    id: UUID


# ---------- Estadio ----------
class EstadioBase(BaseModel):
    nombre: str
    ciudad_id: UUID
    capacidad: int = Field(gt=0)
    disponible: bool = True


class EstadioCreate(EstadioBase):
    pass


class EstadioUpdate(BaseModel):
    nombre: Optional[str] = None
    ciudad_id: Optional[UUID] = None
    capacidad: Optional[int] = None
    disponible: Optional[bool] = None


class Estadio(EstadioBase):
    id: UUID


# ---------- Entrenador ----------
class EntrenadorBase(BaseModel):
    nombre: str
    apellido: str
    nacionalidad: Optional[str] = None


class EntrenadorCreate(EntrenadorBase):
    pass


class EntrenadorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    nacionalidad: Optional[str] = None


class Entrenador(EntrenadorBase):
    id: UUID
