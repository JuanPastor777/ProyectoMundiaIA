"""
Conexión directa a PostgreSQL de Supabase.

La aplicación utiliza PostgreSQL directamente en lugar
de la API REST de Supabase.
"""

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from app.config import settings


# Pool de conexiones
connection_pool = pool.SimpleConnectionPool(
    1,
    10,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
)


def get_connection():
    """
    Obtiene una conexión del pool y configura el esquema mundial.
    """

    connection = connection_pool.getconn()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SET search_path TO {}, public".format(
                    settings.DB_SCHEMA
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        connection_pool.putconn(connection)
        raise

    return connection


def release_connection(connection):
    """
    Devuelve una conexión al pool.
    """

    connection_pool.putconn(connection)


def execute_query(query: str, params=None, fetch=True):
    """
    Ejecuta una consulta SQL y devuelve los resultados
    como diccionarios.
    """

    connection = get_connection()

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:

            cursor.execute(query, params)

            if fetch:
                result = cursor.fetchall()
            else:
                result = None

            connection.commit()

            return result

    except Exception:
        connection.rollback()
        raise

    finally:
        release_connection(connection)