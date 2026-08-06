# Revisión de Código

## Validaciones

- **Pydantic** valida automáticamente los tipos y formatos de entrada en todos los endpoints (fechas, UUIDs, rangos numéricos como `numero_camiseta` entre 1 y 99, `goles >= 0`, etc.).
- **Reglas de negocio adicionales** se validan en la capa de servicios antes de tocar la base de datos: equipos distintos en un partido (`model_validator` en el schema), disponibilidad de estadio (`partidos_service.validar_estadio_disponible`).
- **Restricciones a nivel de base de datos** (UNIQUE, CHECK, FK) actúan como segunda línea de defensa, incluso si la validación de la aplicación fallara.

## Organización del código

- El backend separa responsabilidades en `schemas/` (forma de los datos), `routers/` (endpoints HTTP), `services/` (lógica de negocio y acceso a datos) y `ai/` (agente y tools). Esto facilita ubicar y modificar cada pieza sin afectar a las demás.
- El frontend separa `components/` (piezas reutilizables), `pages/` (una página por sección del menú) y `services/api.js` (único punto de comunicación HTTP con el backend).

## Seguridad

- Ninguna API Key se escribe en el código fuente; todas se leen de variables de entorno.
- El agente IA solo tiene acceso a funciones de lectura (`select`), nunca de escritura.
- CORS está restringido a los orígenes definidos en `CORS_ORIGINS` (por defecto, solo `localhost:5173`).
- Los archivos `.env` están excluidos del control de versiones desde el primer commit.

## Manejo de errores

- El helper `services/crud.py` traduce errores técnicos de PostgreSQL (duplicate key, foreign key, check constraint) a mensajes en español comprensibles para el usuario del frontend.
- Los conflictos de horario de estadio devuelven un código HTTP 409 con un mensaje explícito.
- El endpoint de chat IA devuelve un error controlado (no una caída del servidor) si falta la API Key de OpenAI o si una tool falla al consultar datos.

## Variables de entorno

- Backend: `SUPABASE_URL`, `SUPABASE_KEY`, `OPENAI_API_KEY`, `OPENAI_MODEL`, `CORS_ORIGINS`.
- Frontend: `VITE_API_URL` (y opcionalmente `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY`, no usadas por defecto porque todo pasa por el backend).
- Endpoint `GET /api/salud` permite comprobar rápidamente si falta alguna variable crítica.

## Mejoras posibles

- Agregar autenticación básica para distinguir organizadores de lectores.
- Agregar paginación en los listados cuando el volumen de datos crezca.
- Agregar pruebas automatizadas (pytest) para los tres escenarios Given-When-Then.
- Cachear las respuestas de solo lectura del agente para reducir costo de llamadas a OpenAI en consultas repetidas.
