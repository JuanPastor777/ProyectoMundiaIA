"""
Funciones genéricas para operaciones CRUD contra PostgreSQL.

La conexión se realiza directamente a PostgreSQL de Supabase.
El esquema utilizado por el proyecto es: mundial.
"""

from fastapi import HTTPException
from psycopg2 import sql

from app.database import get_connection, release_connection


def _validar_tabla(tabla: str):
    """
    Valida que el nombre de la tabla sea seguro.
    Evita utilizar nombres arbitrarios en las consultas SQL.
    """

    tablas_permitidas = {
        "ciudades",
        "confederaciones",
        "entrenadores",
        "estadios",
        "estadisticas_jugador",
        "estadisticas_seleccion",
        "grupos",
        "incidencias",
        "jugadores",
        "partidos",
        "selecciones",
    }

    if tabla not in tablas_permitidas:
        raise HTTPException(
            status_code=400,
            detail=f"Tabla no permitida: {tabla}"
        )


def listar(
    tabla: str,
    filtros: dict | None = None,
    orden: str | None = None
):
    """
    Lista todos los registros de una tabla.

    Permite aplicar filtros mediante igualdad y ordenar
    por una columna.
    """

    _validar_tabla(tabla)

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            consulta = sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(tabla)
            )

            valores = []

            if filtros:
                condiciones = []

                for campo, valor in filtros.items():

                    condiciones.append(
                        sql.SQL("{} = %s").format(
                            sql.Identifier(campo)
                        )
                    )

                    valores.append(valor)

                consulta += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(
                    condiciones
                )

            if orden:
                consulta += sql.SQL(" ORDER BY {}").format(
                    sql.Identifier(orden)
                )

            cursor.execute(consulta, valores)

            columnas = [desc[0] for desc in cursor.description]

            registros = [
                dict(zip(columnas, fila))
                for fila in cursor.fetchall()
            ]

            return registros

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=_mensaje_amigable(e)
        )

    finally:
        release_connection(connection)


def obtener_uno(
    tabla: str,
    id_valor: str,
    campo_id: str = "id"
):
    """
    Obtiene un único registro por su identificador.
    """

    _validar_tabla(tabla)

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            consulta = sql.SQL("""
                SELECT *
                FROM {}
                WHERE {} = %s
                LIMIT 1
            """).format(
                sql.Identifier(tabla),
                sql.Identifier(campo_id)
            )

            cursor.execute(
                consulta,
                (id_valor,)
            )

            fila = cursor.fetchone()

            if not fila:
                raise HTTPException(
                    status_code=404,
                    detail=f"Registro no encontrado en {tabla}"
                )

            columnas = [
                desc[0]
                for desc in cursor.description
            ]

            return dict(zip(columnas, fila))

    except HTTPException:
        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=_mensaje_amigable(e)
        )

    finally:
        release_connection(connection)


def crear(tabla: str, datos: dict):
    """
    Inserta un nuevo registro y devuelve el registro creado.
    """

    _validar_tabla(tabla)

    if not datos:
        raise HTTPException(
            status_code=400,
            detail="No se proporcionaron datos para crear el registro."
        )

    connection = get_connection()

    try:

        campos = list(datos.keys())
        valores = list(datos.values())

        columnas_sql = sql.SQL(", ").join(
            sql.Identifier(campo)
            for campo in campos
        )

        placeholders = sql.SQL(", ").join(
            sql.Placeholder()
            for _ in valores
        )

        consulta = sql.SQL("""
            INSERT INTO {}
            ({})
            VALUES ({})
            RETURNING *
        """).format(
            sql.Identifier(tabla),
            columnas_sql,
            placeholders
        )

        with connection.cursor() as cursor:

            cursor.execute(
                consulta,
                valores
            )

            fila = cursor.fetchone()

            columnas = [
                desc[0]
                for desc in cursor.description
            ]

            connection.commit()

            return dict(zip(columnas, fila))

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=_mensaje_amigable(e)
        )

    finally:
        release_connection(connection)


def actualizar(
    tabla: str,
    id_valor: str,
    datos: dict,
    campo_id: str = "id"
):
    """
    Actualiza un registro existente.
    """

    _validar_tabla(tabla)

    datos_limpios = {
        k: v
        for k, v in datos.items()
        if v is not None
    }

    if not datos_limpios:
        raise HTTPException(
            status_code=400,
            detail="No hay datos para actualizar."
        )

    connection = get_connection()

    try:

        campos = list(datos_limpios.keys())
        valores = list(datos_limpios.values())

        asignaciones = sql.SQL(", ").join(
            sql.SQL("{} = %s").format(
                sql.Identifier(campo)
            )
            for campo in campos
        )

        consulta = sql.SQL("""
            UPDATE {}
            SET {}
            WHERE {} = %s
            RETURNING *
        """).format(
            sql.Identifier(tabla),
            asignaciones,
            sql.Identifier(campo_id)
        )

        valores.append(id_valor)

        with connection.cursor() as cursor:

            cursor.execute(
                consulta,
                valores
            )

            fila = cursor.fetchone()

            if not fila:

                connection.rollback()

                raise HTTPException(
                    status_code=404,
                    detail=f"Registro no encontrado en {tabla}"
                )

            columnas = [
                desc[0]
                for desc in cursor.description
            ]

            connection.commit()

            return dict(zip(columnas, fila))

    except HTTPException:
        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=_mensaje_amigable(e)
        )

    finally:
        release_connection(connection)


def eliminar(
    tabla: str,
    id_valor: str,
    campo_id: str = "id"
):
    """
    Elimina un registro.
    """

    _validar_tabla(tabla)

    connection = get_connection()

    try:

        consulta = sql.SQL("""
            DELETE FROM {}
            WHERE {} = %s
            RETURNING *
        """).format(
            sql.Identifier(tabla),
            sql.Identifier(campo_id)
        )

        with connection.cursor() as cursor:

            cursor.execute(
                consulta,
                (id_valor,)
            )

            fila = cursor.fetchone()

            if not fila:

                connection.rollback()

                raise HTTPException(
                    status_code=404,
                    detail=f"Registro no encontrado en {tabla}"
                )

            connection.commit()

            return {
                "eliminado": True
            }

    except HTTPException:
        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=_mensaje_amigable(e)
        )

    finally:
        release_connection(connection)


def _mensaje_amigable(error: Exception) -> str:
    """
    Traduce errores comunes de PostgreSQL
    a mensajes más fáciles de entender.
    """

    msg = str(error)

    if (
        "duplicate key" in msg.lower()
        or "unique constraint" in msg.lower()
    ):
        return (
            "Ya existe un registro con esos datos "
            "(violación de restricción única)."
        )

    if "foreign key" in msg.lower():
        return (
            "La operación referencia un registro que "
            "no existe o está en uso."
        )

    if "check constraint" in msg.lower():
        return (
            "Los datos enviados no cumplen una "
            "regla de validación."
        )

    if "not-null" in msg.lower():
        return (
            "Falta un dato obligatorio para realizar "
            "la operación."
        )

    return msg