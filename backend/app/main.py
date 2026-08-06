from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    confederaciones_grupos,
    estadios,
    entrenadores,
    selecciones,
    jugadores,
    partidos,
    estadisticas,
    ai,
)

app = FastAPI(
    title="API Mundial FIFA 2026",
    description="Sistema web para administrar el Mundial FIFA 2026 (selecciones, jugadores, partidos, estadísticas y agente IA).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(confederaciones_grupos.router)
app.include_router(estadios.router)
app.include_router(entrenadores.router)
app.include_router(selecciones.router)
app.include_router(jugadores.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)
app.include_router(ai.router)


@app.get("/")
def raiz():
    return {"mensaje": "API Mundial FIFA 2026 funcionando correctamente", "docs": "/docs"}


@app.get("/api/salud")
def salud():
    """Endpoint para comprobar rápidamente si faltan variables de entorno."""
    faltantes = settings.validar()
    return {
        "estado": "ok" if not faltantes else "incompleto",
        "variables_faltantes": faltantes,
    }
