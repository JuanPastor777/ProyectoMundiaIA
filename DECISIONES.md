# DECISIONES.md — Sistema Web FIFA Mundial 2026

Documento académico donde se explican las principales decisiones técnicas tomadas durante el desarrollo del proyecto.

## ¿Por qué React?

React permite construir una interfaz de usuario organizada en componentes reutilizables (tablas, formularios, tarjetas del dashboard), lo cual encaja bien con un sistema que repite patrones de "listar / crear / editar / eliminar" en varias secciones (selecciones, jugadores, entrenadores, etc.). Además, es una de las tecnologías más usadas en la industria y en el ámbito académico, con abundante documentación.

## ¿Por qué FastAPI?

FastAPI ofrece tipado con Pydantic (validación automática de datos de entrada), generación automática de documentación interactiva (`/docs`), y un rendimiento adecuado para un proyecto de este tamaño. Su sintaxis es clara y facilita mantener el código organizado en routers, schemas y servicios, como pide el enunciado.

## ¿Por qué Supabase/PostgreSQL?

PostgreSQL es un motor relacional robusto que soporta correctamente las restricciones necesarias (PK, FK, UNIQUE, CHECK) para modelar las reglas del torneo (por ejemplo, evitar que un estadio tenga dos partidos a la misma hora). Supabase ofrece PostgreSQL administrado con una API REST automática (PostgREST) y un panel visual, lo que simplifica la puesta en marcha sin necesidad de administrar un servidor de base de datos manualmente.

## ¿Por qué utilizar un backend en vez de conectar el frontend directamente a Supabase?

Aunque Supabase permite conectarse desde el frontend, hacerlo expondría lógica de negocio sensible (por ejemplo, la actualización de estadísticas al registrar un resultado) y obligaría a duplicar validaciones en el cliente. Centralizar todo en FastAPI permite:
- Mantener la API Key de OpenAI completamente oculta del navegador.
- Aplicar reglas de negocio en un solo lugar (validación de estadio ocupado, actualización de la tabla de posiciones).
- Tener un punto único de control de CORS y manejo de errores.

## ¿Cómo se conecta el agente IA con la base de datos?

El agente no tiene acceso directo a Supabase desde el modelo de lenguaje. En su lugar, se definieron funciones Python de solo lectura (`app/ai/tools.py`) que consultan Supabase y se registran ante OpenAI como *tools* de function calling. Cuando el usuario pregunta algo, el modelo decide qué tool(s) invocar, el backend ejecuta esas funciones contra Supabase, y el resultado (datos reales) se le devuelve al modelo para que redacte la respuesta final en lenguaje natural.

## ¿Por qué el agente no puede modificar información?

Por seguridad y porque el enunciado lo exige explícitamente: un asistente conversacional no debe tener la capacidad de alterar registros oficiales del torneo a partir de una instrucción en lenguaje natural, ya que esto podría producir cambios no auditados o maliciosos. Las funciones expuestas al agente (`tools.py`) están escritas de forma que **solo ejecutan `select`**; no existe ninguna función de escritura disponible para el modelo.

## ¿Cómo se manejan las estadísticas?

Las estadísticas de selección (`estadisticas_seleccion`) se recalculan de forma incremental cada vez que se registra el resultado de un partido (`POST /api/partidos/{id}/resultado`). El servicio `partidos_service.py` determina si el equipo ganó, empató o perdió, y actualiza partidos jugados, goles a favor/en contra y puntos. Esto evita tener que recalcular toda la tabla desde cero en cada consulta.

## ¿Cómo se evita la doble programación de un estadio?

Se aplican **dos capas de protección**:
1. A nivel de aplicación: `partidos_service.validar_estadio_disponible()` consulta si ya existe un partido no cancelado en ese estadio, fecha y hora, y devuelve un error 409 claro antes de intentar guardar.
2. A nivel de base de datos: la tabla `partidos` tiene una restricción `UNIQUE (estadio_id, fecha, hora)`, que actúa como última línea de defensa aunque la validación de la aplicación fallara.

## ¿Cómo se manejan las variables de entorno?

Todas las credenciales (Supabase, OpenAI) se leen desde variables de entorno mediante `python-dotenv` en el backend, y nunca se escriben directamente en archivos `.py`. Se distribuyen archivos `.env.example` con valores ficticios como plantilla, mientras que los archivos `.env` reales están excluidos del control de versiones mediante `.gitignore`. El frontend solo necesita conocer la URL del backend (`VITE_API_URL`); no maneja ninguna credencial sensible.

## ¿Qué limitaciones tiene el sistema?

- No implementa autenticación de usuarios ni roles (organizador/lector), ya que el enunciado no lo exige como prioridad.
- La concurrencia extrema (dos organizadores programando el mismo estadio en el mismo instante) se resuelve por la restricción UNIQUE de la base de datos, pero no hay bloqueo optimista explícito en la aplicación.
- El agente IA depende de la disponibilidad y cuota de la API de OpenAI; si la clave no está configurada, el endpoint `/api/ai/chat` devuelve un error controlado en vez de fallar silenciosamente.
- El sistema no genera reportes en PDF; los "reportes" del agente son respuestas en texto basadas en los datos consultados.
