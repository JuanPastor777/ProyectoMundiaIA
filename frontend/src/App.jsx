import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Selecciones from './pages/Selecciones'
import Jugadores from './pages/Jugadores'
import Entrenadores from './pages/Entrenadores'
import Grupos from './pages/Grupos'
import Estadios from './pages/Estadios'
import Partidos from './pages/Partidos'
import Estadisticas from './pages/Estadisticas'
import Asistente from './pages/Asistente'

export default function App() {
  return (
    <div className="layout">
      <Sidebar />
      <main className="contenido">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/selecciones" element={<Selecciones />} />
          <Route path="/jugadores" element={<Jugadores />} />
          <Route path="/entrenadores" element={<Entrenadores />} />
          <Route path="/grupos" element={<Grupos />} />
          <Route path="/estadios" element={<Estadios />} />
          <Route path="/partidos" element={<Partidos />} />
          <Route path="/estadisticas" element={<Estadisticas />} />
          <Route path="/asistente" element={<Asistente />} />
        </Routes>
      </main>
    </div>
  )
}
