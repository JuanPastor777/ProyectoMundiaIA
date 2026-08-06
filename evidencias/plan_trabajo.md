# Plan de Trabajo

Etapas seguidas para el desarrollo del Sistema Web FIFA Mundial 2026.

## 1. Análisis
- Lectura del caso y del listado de funcionalidades solicitadas.
- Identificación de entidades principales y sus relaciones.
- Definición de las reglas de negocio críticas (estadio no duplicado, equipos distintos, sin estadísticas duplicadas, etc.).

## 2. Diseño de la base de datos
- Modelado de 11 tablas normalizadas.
- Definición de PK, FK, UNIQUE, CHECK e índices.
- Documentación de las relaciones (confederación → selecciones → jugadores/entrenador; grupo → selecciones; ciudad → estadios; estadio/partido → incidencias/estadísticas).

## 3. Configuración de Supabase
- Creación del proyecto en Supabase.
- Ejecución de `schema.sql` y `seed.sql` desde el SQL Editor.
- Obtención de URL y clave de API para el backend.

## 4. Desarrollo backend
- Configuración de FastAPI, CORS y variables de entorno.
- Capa de servicios (`crud.py` genérico, `partidos_service.py` con reglas de negocio).
- Routers REST para cada entidad.
- Endpoint de dashboard y de estadísticas (tabla de posiciones).

## 5. Desarrollo frontend
- Estructura del proyecto con Vite + React Router.
- Componente de navegación lateral.
- Páginas de CRUD para cada entidad, con formularios, tablas y mensajes de éxito/error.
- Página de partidos con registro de resultado en línea.

## 6. Implementación de IA
- Redacción del prompt de sistema del agente (basado en el proporcionado, con mejoras técnicas menores).
- Definición de las tools de solo lectura y su esquema para function calling.
- Bucle de dos llamadas a OpenAI (decisión de tool → ejecución → respuesta final).
- Endpoint `POST /api/ai/chat` y página de chat en el frontend.

## 7. Pruebas
- Verificación manual de los tres escenarios Given-When-Then (ver `funcionamiento.md`).
- Pruebas de los endpoints principales desde `/docs` (Swagger).
- Pruebas de conversación con el agente IA sobre datos del seed.

## 8. Documentación
- Redacción de README, CHECKLIST y DECISIONES.
- Redacción de los documentos de la carpeta `evidencias/`.

## 9. Publicación
- Verificación de `.gitignore` antes del primer commit.
- Subida del repositorio a GitHub.
