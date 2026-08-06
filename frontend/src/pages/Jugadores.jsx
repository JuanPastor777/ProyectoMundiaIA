import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

const VACIO = {
  nombre: '', apellido: '', fecha_nacimiento: '', nacionalidad: '',
  posicion: 'DELANTERO', numero_camiseta: '', seleccion_id: '',
}

export default function Jugadores() {
  const [lista, setLista] = useState([])
  const [selecciones, setSelecciones] = useState([])
  const [form, setForm] = useState(VACIO)
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')

  function cargarTodo() {
    api.get('/api/jugadores').then(setLista).catch((e) => setError(e.message))
    api.get('/api/selecciones').then(setSelecciones).catch(() => {})
  }

  useEffect(cargarTodo, [])

  async function crear(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      await api.post('/api/jugadores', { ...form, numero_camiseta: Number(form.numero_camiseta) })
      setExito('Jugador registrado correctamente.')
      setForm(VACIO)
      cargarTodo()
    } catch (e) {
      setError(e.message)
    }
  }

  async function eliminar(id) {
    setError(''); setExito('')
    try {
      await api.del(`/api/jugadores/${id}`)
      setExito('Jugador eliminado.')
      cargarTodo()
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div>
      <h2>Jugadores</h2>
      <Mensaje tipo="error" texto={error} />
      <Mensaje tipo="exito" texto={exito} />

      <form className="formulario" onSubmit={crear}>
        <label>Nombre</label>
        <input required value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
        <label>Apellido</label>
        <input required value={form.apellido} onChange={(e) => setForm({ ...form, apellido: e.target.value })} />
        <label>Fecha de nacimiento</label>
        <input required type="date" value={form.fecha_nacimiento} onChange={(e) => setForm({ ...form, fecha_nacimiento: e.target.value })} />
        <label>Nacionalidad</label>
        <input value={form.nacionalidad} onChange={(e) => setForm({ ...form, nacionalidad: e.target.value })} />
        <label>Posición</label>
        <select value={form.posicion} onChange={(e) => setForm({ ...form, posicion: e.target.value })}>
          <option value="PORTERO">Portero</option>
          <option value="DEFENSA">Defensa</option>
          <option value="MEDIOCAMPISTA">Mediocampista</option>
          <option value="DELANTERO">Delantero</option>
        </select>
        <label>Número de camiseta</label>
        <input required type="number" min="1" max="99" value={form.numero_camiseta} onChange={(e) => setForm({ ...form, numero_camiseta: e.target.value })} />
        <label>Selección</label>
        <select required value={form.seleccion_id} onChange={(e) => setForm({ ...form, seleccion_id: e.target.value })}>
          <option value="">Selecciona...</option>
          {selecciones.map((s) => <option key={s.id} value={s.id}>{s.nombre}</option>)}
        </select>
        <button type="submit">Registrar jugador</button>
      </form>

      <table>
        <thead><tr><th>Nombre</th><th>Posición</th><th>#</th><th>Selección</th><th></th></tr></thead>
        <tbody>
          {lista.map((j) => (
            <tr key={j.id}>
              <td>{j.nombre} {j.apellido}</td>
              <td>{j.posicion}</td>
              <td>{j.numero_camiseta}</td>
              <td>{selecciones.find((s) => s.id === j.seleccion_id)?.nombre || '—'}</td>
              <td><button className="eliminar" onClick={() => eliminar(j.id)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
