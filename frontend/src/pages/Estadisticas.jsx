import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

export default function Estadisticas() {
  const [tabla, setTabla] = useState([])
  const [selecciones, setSelecciones] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/api/estadisticas').then(setTabla).catch((e) => setError(e.message))
    api.get('/api/selecciones').then(setSelecciones).catch(() => {})
  }, [])

  function nombreSeleccion(id) {
    return selecciones.find((s) => s.id === id)?.nombre || id
  }

  return (
    <div>
      <h2>Tabla de posiciones</h2>
      <Mensaje tipo="error" texto={error} />
      <table>
        <thead>
          <tr>
            <th>Selección</th><th>PJ</th><th>G</th><th>E</th><th>P</th>
            <th>GF</th><th>GC</th><th>DIF</th><th>Pts</th>
          </tr>
        </thead>
        <tbody>
          {tabla.map((f) => (
            <tr key={f.seleccion_id}>
              <td>{nombreSeleccion(f.seleccion_id)}</td>
              <td>{f.partidos_jugados}</td>
              <td>{f.victorias}</td>
              <td>{f.empates}</td>
              <td>{f.derrotas}</td>
              <td>{f.goles_favor}</td>
              <td>{f.goles_contra}</td>
              <td>{f.diferencia_goles}</td>
              <td><strong>{f.puntos}</strong></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
