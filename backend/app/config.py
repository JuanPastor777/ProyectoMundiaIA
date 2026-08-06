"""
Configuración central de la aplicación.

Las credenciales se leen desde variables de entorno
ubicadas en backend/.env.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # PostgreSQL / Supabase
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "postgres")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "mundial")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    def validar(self) -> list[str]:
        """Devuelve las variables de entorno faltantes."""

        faltantes = []

        if not self.DB_HOST:
            faltantes.append("DB_HOST")

        if not self.DB_NAME:
            faltantes.append("DB_NAME")

        if not self.DB_USER:
            faltantes.append("DB_USER")

        if not self.DB_PASSWORD:
            faltantes.append("DB_PASSWORD")

        if not self.OPENAI_API_KEY:
            faltantes.append("OPENAI_API_KEY")

        return faltantes


settings = Settings()