# Análisis del Agente de IA

## Qué hace el agente

El agente es un asistente conversacional pensado para los organizadores del Mundial FIFA 2026. Responde preguntas en lenguaje natural sobre el torneo, consultando siempre información real almacenada en Supabase. No tiene memoria de conversaciones pasadas (cada mensaje se procesa de forma independiente) y no puede modificar ningún dato.

## Qué información consulta

- Partidos: fecha, hora, estadio, selecciones, estado y resultado.
- Selecciones: confederación, grupo, entrenador y lista de jugadores.
- Jugadores: goles acumulados (ranking de goleadores).
- Estadios: disponibilidad en una fecha/hora específica.
- Grupos: tabla de posiciones y partidos asociados (reportes).
- Torneo: total de goles marcados hasta el momento.

## Qué Tools utiliza

Definidas en `backend/app/ai/tools.py` y expuestas a OpenAI vía function calling:

1. **`consultar_partidos`** — Tool 1 del enunciado (gestión de partidos): filtra por fecha, selección o estado.
2. **`consultar_seleccion`** — Tool 2 (selecciones y jugadores): entrenador, confederación, grupo, jugadores.
3. **`consultar_goleadores`** — Tool 2 (jugadores): ranking de goles.
4. **`consultar_disponibilidad_estadio`** — Tool 3 (estadios y reportes): estadios libres en una fecha/hora.
5. **`generar_reporte_grupo`** — Tool 3 (reportes): posiciones y partidos de un grupo.
6. **`consultar_goles_totales_torneo`** — Tool 3 (reportes/estadísticas): total de goles del torneo.

Todas estas funciones ejecutan únicamente `select` contra Supabase.

## Qué restricciones tiene

- No puede ejecutar `INSERT`, `UPDATE` ni `DELETE` — no existe ninguna función de escritura en su conjunto de tools.
- Debe indicar explícitamente cuando la información solicitada no existe, en vez de inventarla (instrucción explícita en el prompt de sistema).
- Debe rechazar amablemente preguntas que no estén relacionadas con el Mundial 2026.
- No revela información privada de usuarios del sistema (el sistema, de todas formas, no maneja datos personales de usuarios administradores).

## Ejemplos de consultas

| Pregunta del organizador | Tool utilizada |
|---|---|
| "¿Qué partidos se juegan el 2026-06-15?" | `consultar_partidos` |
| "¿Cuándo juega Argentina?" | `consultar_partidos` |
| "¿Quién es el entrenador de Brasil?" | `consultar_seleccion` |
| "¿Qué jugadores llevan más goles?" | `consultar_goleadores` |
| "¿Qué estadios están disponibles el 2026-06-20 a las 15:00?" | `consultar_disponibilidad_estadio` |
| "Genera un reporte del Grupo A" | `generar_reporte_grupo` |
| "¿Cuántos goles se han marcado en el torneo?" | `consultar_goles_totales_torneo` |
| "¿Cuál es la capital de Francia?" | Ninguna — el agente responde que solo puede ayudar con temas del Mundial 2026 |

*(Espacio para capturas de pantalla de conversaciones reales con el agente)*
