import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

export default function Dashboard() {
  const [datos, setDatos] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/api/dashboard').then(setDatos).catch((e) => setError(e.message))
  }, [])

  return (
    <div>
      <h2>Dashboard</h2>
      <Mensaje tipo="error" texto={error} />
      {!datos && !error && <p>Cargando...</p>}
      {datos && (
        <>
          <div className="tarjetas">
            <div className="tarjeta"><div className="valor">{datos.total_selecciones}</div><div className="etiqueta">Selecciones</div></div>
            <div className="tarjeta"><div className="valor">{datos.total_jugadores}</div><div className="etiqueta">Jugadores</div></div>
            <div className="tarjeta"><div className="valor">{datos.partidos_programados}</div><div className="etiqueta">Partidos programados</div></div>
            <div className="tarjeta"><div className="valor">{datos.partidos_finalizados}</div><div className="etiqueta">Partidos finalizados</div></div>
            <div className="tarjeta"><div className="valor">{datos.estadios_disponibles}</div><div className="etiqueta">Estadios disponibles</div></div>
            <div className="tarjeta"><div className="valor">{datos.total_goles_torneo}</div><div className="etiqueta">Goles en el torneo</div></div>
          </div>

          <h3>Próximos partidos</h3>
          <table>
            <thead><tr><th>Fecha</th><th>Hora</th><th>Fase</th></tr></thead>
            <tbody>
              {datos.proximos_partidos.length === 0 && (
                <tr><td colSpan="3">No hay partidos programados.</td></tr>
              )}
              {datos.proximos_partidos.map((p) => (
                <tr key={p.id}><td>{p.fecha}</td><td>{p.hora}</td><td>{p.fase}</td></tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  )
}
