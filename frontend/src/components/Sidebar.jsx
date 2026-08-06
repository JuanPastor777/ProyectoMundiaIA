import { NavLink } from 'react-router-dom'

const enlaces = [
  { ruta: '/', etiqueta: 'Dashboard' },
  { ruta: '/selecciones', etiqueta: 'Selecciones' },
  { ruta: '/jugadores', etiqueta: 'Jugadores' },
  { ruta: '/entrenadores', etiqueta: 'Entrenadores' },
  { ruta: '/grupos', etiqueta: 'Grupos' },
  { ruta: '/estadios', etiqueta: 'Estadios' },
  { ruta: '/partidos', etiqueta: 'Partidos' },
  { ruta: '/estadisticas', etiqueta: 'Estadísticas' },
  { ruta: '/asistente', etiqueta: 'Asistente IA' },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h1>🏆 Mundial 2026</h1>
      <nav>
        {enlaces.map((e) => (
          <NavLink
            key={e.ruta}
            to={e.ruta}
            end={e.ruta === '/'}
            className={({ isActive }) => (isActive ? 'activo' : '')}
          >
            {e.etiqueta}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
