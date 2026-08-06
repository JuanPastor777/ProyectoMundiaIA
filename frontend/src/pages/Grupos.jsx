import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

export default function Grupos() {
  const [lista, setLista] = useState([])
  const [nombre, setNombre] = useState('')
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')
  const [seleccionesPorGrupo, setSeleccionesPorGrupo] = useState({})

  function cargar() {
    api.get('/api/grupos').then((gs) => {
      setLista(gs)
      gs.forEach((g) => {
        api.get(`/api/grupos/${g.id}/selecciones`).then((sel) =>
          setSeleccionesPorGrupo((prev) => ({ ...prev, [g.id]: sel }))
        )
      })
    }).catch((e) => setError(e.message))
  }
  useEffect(cargar, [])

  async function crear(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      await api.post('/api/grupos', { nombre })
      setExito('Grupo creado.')
      setNombre('')
      cargar()
    } catch (e) { setError(e.message) }
  }

  return (
    <div>
      <h2>Grupos</h2>
      <Mensaje tipo="error" texto={error} />
      <Mensaje tipo="exito" texto={exito} />

      <form className="formulario" onSubmit={crear}>
        <label>Nombre del grupo (ej. "Grupo A")</label>
        <input required value={nombre} onChange={(e) => setNombre(e.target.value)} />
        <button type="submit">Crear grupo</button>
      </form>

      {lista.map((g) => (
        <div key={g.id} style={{ marginBottom: '1.5rem' }}>
          <h3>{g.nombre}</h3>
          <table>
            <thead><tr><th>Selección</th><th>Código</th></tr></thead>
            <tbody>
              {(seleccionesPorGrupo[g.id] || []).length === 0 && (
                <tr><td colSpan="2">Sin selecciones asignadas todavía.</td></tr>
              )}
              {(seleccionesPorGrupo[g.id] || []).map((s) => (
                <tr key={s.id}><td>{s.nombre}</td><td>{s.codigo}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  )
}
