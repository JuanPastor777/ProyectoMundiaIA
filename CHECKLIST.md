# CHECKLIST — Sistema Web FIFA Mundial 2026

Marca cada elemento a medida que lo verifiques en tu entorno.

## Base de datos y configuración
- [ ] Proyecto creado en Supabase
- [ ] `database/schema.sql` ejecutado sin errores
- [ ] `database/seed.sql` ejecutado sin errores
- [ ] Variables de entorno configuradas en `backend/.env`
- [ ] Variables de entorno configuradas en `frontend/.env`
- [ ] `backend/.env` y `frontend/.env` NO aparecen en `git status`

## Backend
- [ ] `pip install -r requirements.txt` ejecutado sin errores
- [ ] Backend arranca con `uvicorn app.main:app --reload`
- [ ] `GET /api/salud` responde `"estado": "ok"`
- [ ] `GET /docs` muestra la documentación Swagger

## Frontend
- [ ] `npm install` ejecutado sin errores
- [ ] `npm run dev` levanta la app en `http://localhost:5173`
- [ ] El Dashboard muestra datos reales (no errores)

## Funcionalidades
- [ ] CRUD de selecciones
- [ ] CRUD de jugadores
- [ ] Gestión de entrenadores
- [ ] Gestión de grupos (con selecciones asignadas)
- [ ] Gestión de ciudades y estadios
- [ ] Gestión de partidos (programación)
- [ ] Registro de resultados
- [ ] Registro de incidencias
- [ ] Estadísticas de jugadores
- [ ] Tabla de posiciones (estadísticas de selección)

## Agente IA
- [ ] Endpoint `POST /api/ai/chat` funcional
- [ ] Tool de partidos (fecha, selección, estadio, resultado)
- [ ] Tool de selecciones/jugadores/entrenadores/grupos
- [ ] Tool de estadios y reportes
- [ ] El agente indica cuando la información no existe
- [ ] El agente rechaza preguntas fuera del tema del torneo
- [ ] El agente no tiene acceso a INSERT/UPDATE/DELETE

## Reglas de negocio críticas
- [ ] No se permite un partido de una selección contra sí misma
- [ ] No se permite programar dos partidos en el mismo estadio a la misma fecha/hora
- [ ] No se permiten dorsales duplicados dentro de una misma selección
- [ ] No se permiten estadísticas duplicadas del mismo jugador en el mismo partido
- [ ] El resultado 0-0 se guarda correctamente (caso límite)

## Documentación
- [ ] README.md completo
- [ ] CHECKLIST.md (este archivo)
- [ ] DECISIONES.md
- [ ] evidencias/analisis_agente.md
- [ ] evidencias/plan_trabajo.md
- [ ] evidencias/revision_codigo.md
- [ ] evidencias/funcionamiento.md (con capturas de los 3 escenarios)

## Publicación
- [ ] Repositorio creado en GitHub
- [ ] `.gitignore` configurado correctamente antes del primer commit
- [ ] Proyecto subido a GitHub
