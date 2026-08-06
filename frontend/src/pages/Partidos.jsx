import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

const VACIO = {
  fecha: '', hora: '', estadio_id: '', grupo_id: '', fase: 'GRUPOS',
  seleccion_local_id: '', seleccion_visitante_id: '',
}

export default function Partidos() {
  const [lista, setLista] = useState([])
  const [estadios, setEstadios] = useState([])
  const [grupos, setGrupos] = useState([])
  const [selecciones, setSelecciones] = useState([])
  const [form, setForm] = useState(VACIO)
  const [resultados, setResultados] = useState({})
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')

  function cargar() {
    api.get('/api/partidos').then(setLista).catch((e) => setError(e.message))
    api.get('/api/estadios').then(setEstadios).catch(() => {})
    api.get('/api/grupos').then(setGrupos).catch(() => {})
    api.get('/api/selecciones').then(setSelecciones).catch(() => {})
  }
  useEffect(cargar, [])

  function nombreSeleccion(id) {
    return selecciones.find((s) => s.id === id)?.nombre || '—'
  }
  function nombreEstadio(id) {
    return estadios.find((e) => e.id === id)?.nombre || '—'
  }

  async function programar(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      await api.post('/api/partidos', { ...form, grupo_id: form.grupo_id || null })
      setExito('Partido programado correctamente.')
      setForm(VACIO)
      cargar()
    } catch (e) {
      // Este es el caso de error del enunciado: estadio ocupado en el mismo horario
      setError(e.message)
    }
  }

  async function registrarResultado(id) {
    const r = resultados[id]
    if (!r) return
    setError(''); setExito('')
    try {
      await api.post(`/api/partidos/${id}/resultado`, {
        goles_local: Number(r.goles_local ?? 0),
        goles_visitante: Number(r.goles_visitante ?? 0),
      })
      setExito('Resultado registrado. Estadísticas actualizadas.')
      cargar()
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div>
      <h2>Partidos</h2>
      <Mensaje tipo="error" texto={error} />
      <Mensaje tipo="exito" texto={exito} />

      <form className="formulario" onSubmit={programar}>
        <strong>Programar partido</strong>
        <label>Fecha</label>
        <input required type="date" value={form.fecha} onChange={(e) => setForm({ ...form, fecha: e.target.value })} />
        <label>Hora</label>
        <input required type="time" value={form.hora} onChange={(e) => setForm({ ...form, hora: e.target.value })} />
        <label>Estadio</label>
        <select required value={form.estadio_id} onChange={(e) => setForm({ ...form, estadio_id: e.target.value })}>
          <option value="">Selecciona...</option>
          {estadios.map((e) => <option key={e.id} value={e.id}>{e.nombre}</option>)}
        </select>
        <label>Grupo (opcional)</label>
        <select value={form.grupo_id} onChange={(e) => setForm({ ...form, grupo_id: e.target.value })}>
          <option value="">Sin grupo</option>
          {grupos.map((g) => <option key={g.id} value={g.id}>{g.nombre}</option>)}
        </select>
        <label>Fase</label>
        <select value={form.fase} onChange={(e) => setForm({ ...form, fase: e.target.value })}>
          <option value="GRUPOS">Grupos</option>
          <option value="OCTAVOS">Octavos</option>
          <option value="CUARTOS">Cuartos</option>
          <option value="SEMIFINAL">Semifinal</option>
          <option value="TERCER_PUESTO">Tercer puesto</option>
          <option value="FINAL">Final</option>
        </select>
        <label>Selección local</label>
        <select required value={form.seleccion_local_id} onChange={(e) => setForm({ ...form, seleccion_local_id: e.target.value })}>
          <option value="">Selecciona...</option>
          {selecciones.map((s) => <option key={s.id} value={s.id}>{s.nombre}</option>)}
        </select>
        <label>Selección visitante</label>
        <select required value={form.seleccion_visitante_id} onChange={(e) => setForm({ ...form, seleccion_visitante_id: e.target.value })}>
          <option value="">Selecciona...</option>
          {selecciones.map((s) => <option key={s.id} value={s.id}>{s.nombre}</option>)}
        </select>
        <button type="submit">Programar</button>
      </form>

      <table>
        <thead>
          <tr><th>Fecha</th><th>Hora</th><th>Estadio</th><th>Partido</th><th>Estado</th><th>Marcador</th><th>Registrar resultado</th></tr>
        </thead>
        <tbody>
          {lista.map((p) => (
            <tr key={p.id}>
              <td>{p.fecha}</td>
              <td>{p.hora}</td>
              <td>{nombreEstadio(p.estadio_id)}</td>
              <td>{nombreSeleccion(p.seleccion_local_id)} vs {nombreSeleccion(p.seleccion_visitante_id)}</td>
              <td>{p.estado}</td>
              <td>{p.estado === 'FINALIZADO' ? `${p.goles_local} - ${p.goles_visitante}` : '—'}</td>
              <td>
                {p.estado !== 'FINALIZADO' && p.estado !== 'CANCELADO' ? (
                  <div style={{ display: 'flex', gap: '0.25rem', alignItems: 'center' }}>
                    <input type="number" min="0" placeholder="Local" style={{ width: '55px' }}
                      onChange={(e) => setResultados({ ...resultados, [p.id]: { ...resultados[p.id], goles_local: e.target.value } })} />
                    <input type="number" min="0" placeholder="Visit." style={{ width: '55px' }}
                      onChange={(e) => setResultados({ ...resultados, [p.id]: { ...resultados[p.id], goles_visitante: e.target.value } })} />
                    <button onClick={() => registrarResultado(p.id)}>Guardar</button>
                  </div>
                ) : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
