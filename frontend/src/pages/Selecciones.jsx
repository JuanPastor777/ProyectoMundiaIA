import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

const VACIO = { nombre: '', codigo: '', confederacion_id: '', grupo_id: '', entrenador_id: '' }

export default function Selecciones() {
  const [lista, setLista] = useState([])
  const [confederaciones, setConfederaciones] = useState([])
  const [grupos, setGrupos] = useState([])
  const [entrenadores, setEntrenadores] = useState([])
  const [form, setForm] = useState(VACIO)
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')

  function cargarTodo() {
    api.get('/api/selecciones').then(setLista).catch((e) => setError(e.message))
    api.get('/api/confederaciones').then(setConfederaciones).catch(() => {})
    api.get('/api/grupos').then(setGrupos).catch(() => {})
    api.get('/api/entrenadores').then(setEntrenadores).catch(() => {})
  }

  useEffect(cargarTodo, [])

  async function crear(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      const payload = {
        nombre: form.nombre,
        codigo: form.codigo.toUpperCase(),
        confederacion_id: form.confederacion_id,
        grupo_id: form.grupo_id || null,
        entrenador_id: form.entrenador_id || null,
      }
      await api.post('/api/selecciones', payload)
      setExito('Selección creada correctamente.')
      setForm(VACIO)
      cargarTodo()
    } catch (e) {
      setError(e.message)
    }
  }

  async function eliminar(id) {
    setError(''); setExito('')
    try {
      await api.del(`/api/selecciones/${id}`)
      setExito('Selección eliminada.')
      cargarTodo()
    } catch (e) {
      setError(e.message)
    }
  }

  function nombrePorId(arr, id) {
    return arr.find((x) => x.id === id)?.nombre || '—'
  }

  return (
    <div>
      <h2>Selecciones</h2>
      <Mensaje tipo="error" texto={error} />
      <Mensaje tipo="exito" texto={exito} />

      <form className="formulario" onSubmit={crear}>
        <label>Nombre</label>
        <input required value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />

        <label>Código (3 letras)</label>
        <input required maxLength={3} value={form.codigo} onChange={(e) => setForm({ ...form, codigo: e.target.value })} />

        <label>Confederación</label>
        <select required value={form.confederacion_id} onChange={(e) => setForm({ ...form, confederacion_id: e.target.value })}>
          <option value="">Selecciona...</option>
          {confederaciones.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>

        <label>Grupo (opcional)</label>
        <select value={form.grupo_id} onChange={(e) => setForm({ ...form, grupo_id: e.target.value })}>
          <option value="">Sin grupo</option>
          {grupos.map((g) => <option key={g.id} value={g.id}>{g.nombre}</option>)}
        </select>

        <label>Entrenador (opcional)</label>
        <select value={form.entrenador_id} onChange={(e) => setForm({ ...form, entrenador_id: e.target.value })}>
          <option value="">Sin entrenador</option>
          {entrenadores.map((en) => <option key={en.id} value={en.id}>{en.nombre} {en.apellido}</option>)}
        </select>

        <button type="submit">Crear selección</button>
      </form>

      <table>
        <thead><tr><th>Nombre</th><th>Código</th><th>Confederación</th><th>Grupo</th><th>Entrenador</th><th></th></tr></thead>
        <tbody>
          {lista.map((s) => (
            <tr key={s.id}>
              <td>{s.nombre}</td>
              <td>{s.codigo}</td>
              <td>{nombrePorId(confederaciones, s.confederacion_id)}</td>
              <td>{nombrePorId(grupos, s.grupo_id)}</td>
              <td>{entrenadores.find((e) => e.id === s.entrenador_id) ? `${entrenadores.find((e) => e.id === s.entrenador_id).nombre} ${entrenadores.find((e) => e.id === s.entrenador_id).apellido}` : '—'}</td>
              <td><button className="eliminar" onClick={() => eliminar(s.id)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
