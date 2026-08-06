# Sistema Web FIFA Mundial 2026

## 1. Descripción del proyecto

Aplicación web full-stack para que la FIFA administre el Mundial 2026: selecciones, jugadores, entrenadores, grupos, confederaciones, ciudades, estadios, calendario de partidos, resultados, incidencias y estadísticas del torneo. Incluye un **agente de inteligencia artificial** que responde consultas de los organizadores usando únicamente datos reales almacenados en la base de datos.

## 2. Objetivo

Ofrecer un sistema claro y funcional (apropiado para un proyecto universitario) que centralice la administración del torneo y facilite la consulta de información mediante un asistente conversacional, sin exponer credenciales ni permitir que la IA modifique datos.

## 3. Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Frontend | React 18 + Vite + React Router |
| Backend | Python 3.11+ + FastAPI |
| Base de datos | PostgreSQL alojado en Supabase |
| IA | API de OpenAI (function calling) |
| Control de versiones | Git + GitHub |

## 4. Arquitectura

```
Frontend (React)  →  Backend (FastAPI)  →  Supabase (PostgreSQL)
                              ↓
                        Agente IA  →  OpenAI API
```

El frontend **nunca** llama a OpenAI ni a Supabase directamente para operaciones sensibles: todo pasa por FastAPI, que es el único lugar donde viven las claves privadas.

## 5. Estructura de carpetas

```
mundial-2026/
├── frontend/          # React + Vite
│   └── src/
│       ├── components/  (Sidebar, Mensaje)
│       ├── pages/       (Dashboard, Selecciones, Jugadores, ...)
│       └── services/    (api.js — cliente HTTP hacia FastAPI)
├── backend/
│   └── app/
│       ├── main.py       # arranque de FastAPI + routers
│       ├── config.py     # variables de entorno
│       ├── database.py   # cliente de Supabase
│       ├── schemas/      # modelos Pydantic
│       ├── routers/      # endpoints REST
│       ├── services/     # lógica de negocio (CRUD genérico, partidos)
│       └── ai/           # agente IA (tools.py, agent.py)
├── database/
│   ├── schema.sql   # estructura completa de la BD
│   └── seed.sql     # datos de prueba
├── evidencias/       # documentación de análisis, plan, revisión y pruebas
├── README.md
├── CHECKLIST.md
├── DECISIONES.md
└── .gitignore
```

## 6. Configuración de Supabase

1. Crea una cuenta y un proyecto en [supabase.com](https://supabase.com).
2. Ve a **SQL Editor > New query**, pega el contenido completo de `database/schema.sql` y ejecútalo.
3. Repite el paso anterior con `database/seed.sql` para cargar los datos de prueba.
4. Ve a **Project Settings > API** y copia:
   - **Project URL** → será tu `SUPABASE_URL`.
   - **anon public key** (o **service_role**, si prefieres más permisos desde el backend) → será tu `SUPABASE_KEY`.

## 7. Configuración del `.env`

**Backend** (`backend/.env`, cópialo desde `backend/.env.example`):
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_clave_real
OPENAI_API_KEY=tu_api_key_real
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=http://localhost:5173
```

**Frontend** (`frontend/.env`, cópialo desde `frontend/.env.example`):
```env
VITE_API_URL=http://localhost:8000
```

⚠️ Los archivos `.env` reales **no se suben a GitHub** (ya están en `.gitignore`). Solo se suben los `.env.example` con valores ficticios.

## 8. Instalación del backend (Windows / macOS / Linux)

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env      # Windows
# cp .env.example .env      # macOS/Linux
```

Edita `backend/.env` y coloca tus credenciales reales.

## 9. Instalación del frontend

```bash
cd frontend
npm install
copy .env.example .env      # Windows
# cp .env.example .env      # macOS/Linux
```

## 10. Cómo ejecutar el proyecto

En dos terminales distintas:

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate        # Windows (o "source venv/bin/activate" en macOS/Linux)
uvicorn app.main:app --reload --port 8000
```

```bash
# Terminal 2 - Frontend
cd frontend
npm run dev
```

- Backend: http://localhost:8000 (documentación interactiva en http://localhost:8000/docs)
- Frontend: http://localhost:5173

## 11. Cómo crear las tablas

Ejecuta `database/schema.sql` completo en el **SQL Editor** de Supabase (ver sección 6).

## 12. Cómo cargar datos de prueba

Ejecuta `database/seed.sql` completo en el **SQL Editor** de Supabase, después del schema.

## 13. Cómo utilizar el agente IA

1. Abre el frontend y entra a la sección **Asistente IA**.
2. Escribe una pregunta relacionada con el torneo, por ejemplo:
   - "¿Cuándo juega Argentina?"
   - "¿Quién es el entrenador de Brasil?"
   - "¿Qué estadios están disponibles el 2026-06-20 a las 15:00?"
   - "Genera un reporte del Grupo A"
   - "¿Cuántos goles se han marcado en el torneo?"
3. El backend consulta Supabase mediante *tools* de solo lectura y OpenAI redacta la respuesta con esos datos reales. Si la información no existe, el agente lo indica en vez de inventarla. Si la pregunta no tiene relación con el Mundial, el agente lo indicará amablemente.

## 14. Endpoints principales

```
GET/POST/PUT/DELETE  /api/selecciones[/{id}]
GET                   /api/selecciones/{id}/jugadores
GET/POST/PUT/DELETE  /api/jugadores[/{id}]
GET/POST             /api/entrenadores
GET/POST             /api/grupos
GET                   /api/grupos/{id}/selecciones
GET                   /api/grupos/{id}/partidos
GET/POST             /api/ciudades
GET/POST/PUT/DELETE  /api/estadios[/{id}]
GET                   /api/estadios/disponibilidad?fecha=YYYY-MM-DD&hora=HH:MM
GET/POST/PUT         /api/partidos[/{id}]
POST                  /api/partidos/{id}/resultado
POST/GET              /api/partidos/{id}/incidencias
GET                   /api/estadisticas          (tabla de posiciones)
GET                   /api/estadisticas/jugadores
GET                   /api/dashboard
POST                  /api/ai/chat
GET                   /api/salud                 (comprueba variables de entorno)
```

Documentación interactiva completa (Swagger) en `/docs` una vez el backend está corriendo.

## 15. Cómo publicar en GitHub

```bash
git init
git add .
git commit -m "Sistema Web FIFA Mundial 2026 - versión inicial"
git branch -M main
git remote add origin https://github.com/tu-usuario/mundial-2026.git
git push -u origin main
```

Antes de hacer el primer commit, verifica con `git status` que **no aparezca ningún archivo `.env`** (solo deben aparecer los `.env.example`).

## Comprobaciones rápidas

- **¿FastAPI está conectado a Supabase?** Visita `http://localhost:8000/api/salud`; si `variables_faltantes` está vacío y `/api/selecciones` devuelve datos del seed, la conexión funciona.
- **¿React se comunica con FastAPI?** Abre el Dashboard del frontend; si ves números (no un mensaje de error), la comunicación funciona.
- **¿El agente consulta datos reales?** Pregúntale por una selección que exista en el seed (ej. "Argentina") y verifica que los datos coincidan con lo que ves en la sección Selecciones.
