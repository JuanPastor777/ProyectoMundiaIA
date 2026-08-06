-- =====================================================================
-- MUNDIAL 2026 - SCHEMA DE BASE DE DATOS (PostgreSQL / Supabase)
-- =====================================================================
-- Ejecutar este archivo completo en: Supabase > SQL Editor > New query
-- =====================================================================

-- Extensión para UUID (Supabase normalmente ya la tiene habilitada)
create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------
-- 1. CONFEDERACIONES
-- ---------------------------------------------------------------------
create table confederaciones (
    id              uuid primary key default gen_random_uuid(),
    nombre          varchar(100) not null unique,
    codigo          varchar(10)  not null unique,
    creado_en       timestamptz  not null default now()
);

-- ---------------------------------------------------------------------
-- 2. GRUPOS (Grupo A, B, C... del torneo)
-- ---------------------------------------------------------------------
create table grupos (
    id              uuid primary key default gen_random_uuid(),
    nombre          varchar(50) not null unique,   -- 'Grupo A'
    creado_en       timestamptz not null default now()
);

-- ---------------------------------------------------------------------
-- 3. CIUDADES
-- ---------------------------------------------------------------------
create table ciudades (
    id              uuid primary key default gen_random_uuid(),
    nombre          varchar(100) not null,
    pais            varchar(100) not null,
    creado_en       timestamptz not null default now(),
    unique (nombre, pais)
);

-- ---------------------------------------------------------------------
-- 4. ESTADIOS
-- ---------------------------------------------------------------------
create table estadios (
    id              uuid primary key default gen_random_uuid(),
    nombre          varchar(150) not null unique,
    ciudad_id       uuid not null references ciudades(id) on delete restrict,
    capacidad       integer not null check (capacidad > 0),
    disponible      boolean not null default true,
    creado_en       timestamptz not null default now()
);
create index idx_estadios_ciudad on estadios(ciudad_id);

-- ---------------------------------------------------------------------
-- 5. ENTRENADORES
-- ---------------------------------------------------------------------
create table entrenadores (
    id              uuid primary key default gen_random_uuid(),
    nombre          varchar(100) not null,
    apellido        varchar(100) not null,
    nacionalidad    varchar(100),
    creado_en       timestamptz not null default now()
);

-- ---------------------------------------------------------------------
-- 6. SELECCIONES
-- ---------------------------------------------------------------------
create table selecciones (
    id                  uuid primary key default gen_random_uuid(),
    nombre              varchar(100) not null unique,
    codigo              varchar(3)   not null unique,   -- 'ARG', 'BRA'
    confederacion_id    uuid not null references confederaciones(id) on delete restrict,
    grupo_id            uuid references grupos(id) on delete set null,
    entrenador_id       uuid references entrenadores(id) on delete set null,
    creado_en           timestamptz not null default now()
);
create index idx_selecciones_confederacion on selecciones(confederacion_id);
create index idx_selecciones_grupo on selecciones(grupo_id);

-- ---------------------------------------------------------------------
-- 7. JUGADORES
-- ---------------------------------------------------------------------
create table jugadores (
    id                  uuid primary key default gen_random_uuid(),
    nombre              varchar(100) not null,
    apellido            varchar(100) not null,
    fecha_nacimiento    date not null,
    nacionalidad        varchar(100),
    posicion            varchar(30) not null check (posicion in
                            ('PORTERO','DEFENSA','MEDIOCAMPISTA','DELANTERO')),
    numero_camiseta     integer not null check (numero_camiseta between 1 and 99),
    seleccion_id        uuid not null references selecciones(id) on delete cascade,
    creado_en           timestamptz not null default now(),
    -- Un mismo dorsal no se puede repetir dentro de la misma selección
    unique (seleccion_id, numero_camiseta)
);
create index idx_jugadores_seleccion on jugadores(seleccion_id);

-- ---------------------------------------------------------------------
-- 8. PARTIDOS
-- ---------------------------------------------------------------------
create table partidos (
    id                  uuid primary key default gen_random_uuid(),
    fecha               date not null,
    hora                time not null,
    estadio_id          uuid not null references estadios(id) on delete restrict,
    grupo_id            uuid references grupos(id) on delete set null,
    fase                varchar(50) not null default 'GRUPOS' check (fase in
                            ('GRUPOS','OCTAVOS','CUARTOS','SEMIFINAL','FINAL','TERCER_PUESTO')),
    seleccion_local_id     uuid not null references selecciones(id) on delete restrict,
    seleccion_visitante_id uuid not null references selecciones(id) on delete restrict,
    estado              varchar(20) not null default 'PROGRAMADO' check (estado in
                            ('PROGRAMADO','EN_CURSO','FINALIZADO','CANCELADO')),
    goles_local          integer check (goles_local >= 0),
    goles_visitante       integer check (goles_visitante >= 0),
    creado_en            timestamptz not null default now(),
    actualizado_en       timestamptz not null default now(),

    -- Regla 1: una selección no puede jugar contra sí misma
    constraint chk_equipos_distintos check (seleccion_local_id <> seleccion_visitante_id),

    -- Regla 2: no se puede programar dos partidos en el mismo estadio, fecha y hora
    constraint uq_estadio_fecha_hora unique (estadio_id, fecha, hora)
);
create index idx_partidos_estadio on partidos(estadio_id);
create index idx_partidos_fecha on partidos(fecha);
create index idx_partidos_local on partidos(seleccion_local_id);
create index idx_partidos_visitante on partidos(seleccion_visitante_id);

-- Trigger para mantener actualizado_en al día
create or replace function set_actualizado_en()
returns trigger as $$
begin
    new.actualizado_en = now();
    return new;
end;
$$ language plpgsql;

create trigger trg_partidos_actualizado
before update on partidos
for each row execute function set_actualizado_en();

-- ---------------------------------------------------------------------
-- 9. INCIDENCIAS (goles, tarjetas, sustituciones, lesiones, etc.)
-- ---------------------------------------------------------------------
create table incidencias (
    id              uuid primary key default gen_random_uuid(),
    partido_id      uuid not null references partidos(id) on delete cascade,
    jugador_id      uuid references jugadores(id) on delete set null,
    minuto          integer not null check (minuto between 0 and 130),
    tipo            varchar(30) not null check (tipo in
                        ('GOL','TARJETA_AMARILLA','TARJETA_ROJA','SUSTITUCION',
                         'LESION','PENAL','AUTOGOL')),
    descripcion     text,
    creado_en       timestamptz not null default now()
);
create index idx_incidencias_partido on incidencias(partido_id);
create index idx_incidencias_jugador on incidencias(jugador_id);

-- ---------------------------------------------------------------------
-- 10. ESTADÍSTICAS DE JUGADORES POR PARTIDO
-- ---------------------------------------------------------------------
create table estadisticas_jugador (
    id                  uuid primary key default gen_random_uuid(),
    jugador_id          uuid not null references jugadores(id) on delete cascade,
    partido_id          uuid not null references partidos(id) on delete cascade,
    goles               integer not null default 0 check (goles >= 0),
    asistencias         integer not null default 0 check (asistencias >= 0),
    tarjetas_amarillas  integer not null default 0 check (tarjetas_amarillas in (0,1)),
    tarjetas_rojas      integer not null default 0 check (tarjetas_rojas in (0,1)),
    minutos_jugados     integer not null default 0 check (minutos_jugados between 0 and 130),
    creado_en           timestamptz not null default now(),

    -- Regla 5: no duplicar estadísticas del mismo jugador en el mismo partido
    unique (jugador_id, partido_id)
);
create index idx_estjug_jugador on estadisticas_jugador(jugador_id);
create index idx_estjug_partido on estadisticas_jugador(partido_id);

-- ---------------------------------------------------------------------
-- 11. ESTADÍSTICAS DE SELECCIONES (tabla de posiciones, se recalcula)
-- ---------------------------------------------------------------------
create table estadisticas_seleccion (
    id                      uuid primary key default gen_random_uuid(),
    seleccion_id            uuid not null references selecciones(id) on delete cascade unique,
    partidos_jugados        integer not null default 0,
    victorias               integer not null default 0,
    empates                 integer not null default 0,
    derrotas                integer not null default 0,
    goles_favor             integer not null default 0,
    goles_contra            integer not null default 0,
    puntos                  integer not null default 0,
    actualizado_en          timestamptz not null default now()
);

-- =====================================================================
-- FIN DEL SCHEMA
-- =====================================================================
