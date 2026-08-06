# Funcionamiento — Casos de Prueba

## Caso exitoso

**Given:** Existe un partido programado entre Argentina y Brasil (ver `seed.sql`, partido `77777777-...-701`, ya se usó como ejemplo finalizado).

**When:** El organizador llama a `POST /api/partidos/{id}/resultado` con `{"goles_local": 2, "goles_visitante": 1}` (o lo hace desde la sección Partidos del frontend).

**Then:**
- El partido queda con `estado = FINALIZADO` y el marcador guardado.
- `estadisticas_seleccion` se actualiza para ambas selecciones (partidos jugados, victoria/derrota, goles a favor/contra, puntos).
- `GET /api/estadisticas` refleja el cambio inmediatamente en la tabla de posiciones.

*(Espacio para captura de pantalla: respuesta del endpoint / tabla de posiciones actualizada)*

## Caso de error

**Given:** Un organizador intenta registrar un partido nuevo.

**When:** Selecciona un estadio, fecha y hora que ya están ocupados por otro partido no cancelado (`POST /api/partidos` con esos datos).

**Then:**
- El backend responde `409 Conflict` con el mensaje: *"El estadio seleccionado ya tiene un partido programado en esa fecha y hora."*
- El partido NO se guarda en la base de datos.
- El frontend muestra el mensaje de error en el formulario de programación de partidos.

*(Espacio para captura de pantalla: mensaje de error en el formulario)*

## Caso límite

**Given:** Un partido programado (por ejemplo, Francia vs Argentina) termina sin goles.

**When:** El organizador registra el marcador `0-0` mediante `POST /api/partidos/{id}/resultado` con `{"goles_local": 0, "goles_visitante": 0}`.

**Then:**
- El sistema acepta el marcador (0 es un valor válido según el `CHECK (goles_local >= 0)`).
- El partido queda `FINALIZADO` con `goles_local = 0` y `goles_visitante = 0`.
- Ambas selecciones reciben un empate (+1 punto cada una) en `estadisticas_seleccion`.
- No se registra ningún anotador porque no hubo incidencias de tipo `GOL`.

*(Espacio para captura de pantalla: partido 0-0 guardado y reflejado en la tabla de posiciones)*

## Consultas al agente IA

*(Espacio para capturas de pantalla de conversaciones reales)*

Ejemplos sugeridos a probar:
1. "¿Cuándo juega Argentina?" → debe usar `consultar_partidos` y responder con fecha, hora y rival.
2. "¿Quién es el entrenador de Brasil?" → debe usar `consultar_seleccion`.
3. "Genera un reporte del Grupo A" → debe usar `generar_reporte_grupo` y mostrar posiciones.
4. "¿Cuál es la capital de Francia?" → debe rechazar la pregunta por no estar relacionada con el torneo.
5. Preguntar por una selección que no existe en el seed → debe indicar que no hay información registrada, sin inventar datos.
