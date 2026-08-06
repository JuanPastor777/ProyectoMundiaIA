-- =====================================================================
-- MUNDIAL 2026 - DATOS DE PRUEBA (seed)
-- =====================================================================
-- Ejecutar DESPUÉS de schema.sql, en Supabase > SQL Editor
-- =====================================================================

-- 1. Confederaciones
insert into confederaciones (id, nombre, codigo) values
 ('11111111-1111-1111-1111-111111111101', 'Confederación Sudamericana de Fútbol', 'CONMEBOL'),
 ('11111111-1111-1111-1111-111111111102', 'Unión Europea de Fútbol Asociado', 'UEFA'),
 ('11111111-1111-1111-1111-111111111103', 'Confederación de Norte/Centroamérica y el Caribe', 'CONCACAF');

-- 2. Grupos
insert into grupos (id, nombre) values
 ('22222222-2222-2222-2222-222222222201', 'Grupo A'),
 ('22222222-2222-2222-2222-222222222202', 'Grupo B');

-- 3. Ciudades
insert into ciudades (id, nombre, pais) values
 ('33333333-3333-3333-3333-333333333301', 'Ciudad de México', 'México'),
 ('33333333-3333-3333-3333-333333333302', 'Nueva York', 'Estados Unidos'),
 ('33333333-3333-3333-3333-333333333303', 'Toronto', 'Canadá');

-- 4. Estadios
insert into estadios (id, nombre, ciudad_id, capacidad, disponible) values
 ('44444444-4444-4444-4444-444444444401', 'Estadio Azteca', '33333333-3333-3333-3333-333333333301', 87523, true),
 ('44444444-4444-4444-4444-444444444402', 'MetLife Stadium', '33333333-3333-3333-3333-333333333302', 82500, true),
 ('44444444-4444-4444-4444-444444444403', 'BMO Field', '33333333-3333-3333-3333-333333333303', 30000, true);

-- 5. Entrenadores
insert into entrenadores (id, nombre, apellido, nacionalidad) values
 ('55555555-5555-5555-5555-555555555501', 'Lionel', 'Scaloni', 'Argentina'),
 ('55555555-5555-5555-5555-555555555502', 'Dorival', 'Júnior', 'Brasil'),
 ('55555555-5555-5555-5555-555555555503', 'Didier', 'Deschamps', 'Francia');

-- 6. Selecciones
insert into selecciones (id, nombre, codigo, confederacion_id, grupo_id, entrenador_id) values
 ('66666666-6666-6666-6666-666666666601', 'Argentina', 'ARG',
   '11111111-1111-1111-1111-111111111101', '22222222-2222-2222-2222-222222222201', '55555555-5555-5555-5555-555555555501'),
 ('66666666-6666-6666-6666-666666666602', 'Brasil', 'BRA',
   '11111111-1111-1111-1111-111111111101', '22222222-2222-2222-2222-222222222201', '55555555-5555-5555-5555-555555555502'),
 ('66666666-6666-6666-6666-666666666603', 'Francia', 'FRA',
   '11111111-1111-1111-1111-111111111102', '22222222-2222-2222-2222-222222222202', '55555555-5555-5555-5555-555555555503');

-- 7. Jugadores
insert into jugadores (nombre, apellido, fecha_nacimiento, nacionalidad, posicion, numero_camiseta, seleccion_id) values
 ('Lionel', 'Messi', '1987-06-24', 'Argentina', 'DELANTERO', 10, '66666666-6666-6666-6666-666666666601'),
 ('Emiliano', 'Martínez', '1992-09-02', 'Argentina', 'PORTERO', 23, '66666666-6666-6666-6666-666666666601'),
 ('Vinícius', 'Júnior', '2000-07-12', 'Brasil', 'DELANTERO', 7, '66666666-6666-6666-6666-666666666602'),
 ('Alisson', 'Becker', '1992-10-02', 'Brasil', 'PORTERO', 1, '66666666-6666-6666-6666-666666666602'),
 ('Kylian', 'Mbappé', '1998-12-20', 'Francia', 'DELANTERO', 7, '66666666-6666-6666-6666-666666666603');

-- 8. Partidos (uno finalizado, uno programado)
insert into partidos (id, fecha, hora, estadio_id, grupo_id, fase, seleccion_local_id, seleccion_visitante_id, estado, goles_local, goles_visitante) values
 ('77777777-7777-7777-7777-777777777701', '2026-06-15', '18:00', '44444444-4444-4444-4444-444444444401',
   '22222222-2222-2222-2222-222222222201', 'GRUPOS',
   '66666666-6666-6666-6666-666666666601', '66666666-6666-6666-6666-666666666602', 'FINALIZADO', 2, 1),
 ('77777777-7777-7777-7777-777777777702', '2026-06-20', '15:00', '44444444-4444-4444-4444-444444444402',
   '22222222-2222-2222-2222-222222222201', 'GRUPOS',
   '66666666-6666-6666-6666-666666666603', '66666666-6666-6666-6666-666666666601', 'PROGRAMADO', null, null);

-- 9. Incidencias del partido finalizado
insert into incidencias (partido_id, jugador_id, minuto, tipo, descripcion) values
 ('77777777-7777-7777-7777-777777777701',
   (select id from jugadores where numero_camiseta = 10 and seleccion_id = '66666666-6666-6666-6666-666666666601'),
   23, 'GOL', 'Gol de Messi tras jugada individual'),
 ('77777777-7777-7777-7777-777777777701',
   (select id from jugadores where numero_camiseta = 7 and seleccion_id = '66666666-6666-6666-6666-666666666602'),
   67, 'GOL', 'Gol de Vinícius Júnior');

-- 10. Estadísticas de jugadores para el partido finalizado
insert into estadisticas_jugador (jugador_id, partido_id, goles, asistencias, tarjetas_amarillas, tarjetas_rojas, minutos_jugados) values
 ((select id from jugadores where numero_camiseta = 10 and seleccion_id = '66666666-6666-6666-6666-666666666601'),
   '77777777-7777-7777-7777-777777777701', 1, 0, 0, 0, 90),
 ((select id from jugadores where numero_camiseta = 7 and seleccion_id = '66666666-6666-6666-6666-666666666602'),
   '77777777-7777-7777-7777-777777777701', 1, 0, 0, 0, 90);

-- 11. Estadísticas de selecciones (resultado del partido ya reflejado)
insert into estadisticas_seleccion (seleccion_id, partidos_jugados, victorias, empates, derrotas, goles_favor, goles_contra, puntos) values
 ('66666666-6666-6666-6666-666666666601', 1, 1, 0, 0, 2, 1, 3),
 ('66666666-6666-6666-6666-666666666602', 1, 0, 0, 1, 1, 2, 0),
 ('66666666-6666-6666-6666-666666666603', 0, 0, 0, 0, 0, 0, 0);
