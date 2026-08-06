import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

const VACIO = { nombre: '', ciudad_id: '', capacidad: '', disponible: true }
const CIUDAD_VACIA = { nombre: '', pais: '' }

export default function Estadios() {
  const [lista, setLista] = useState([])
  const [ciudades, setCiudades] = useState([])
  const [form, setForm] = useState(VACIO)
  const [formCiudad, setFormCiudad] = useState(CIUDAD_VACIA)
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')

  function cargar() {
    api.get('/api/estadios').then(setLista).catch((e) => setError(e.message))
    api.get('/api/ciudades').then(setCiudades).catch(() => {})
  }
  useEffect(cargar, [])

  async function crearCiudad(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      await api.post('/api/ciudades', formCiudad)
      setExito('Ciudad creada.')
      setFormCiudad(CIUDAD_VACIA)
      cargar()
    } catch (e) { setError(e.message) }
  }

  async function crear(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      await api.post('/api/estadios', { ...form, capacidad: Number(form.capacidad) })
      setExito('Estadio creado.')
      setForm(VACIO)
      cargar()
    } catch (e) { setError(e.message) }
  }

  async function eliminar(id) {
    setError(''); setExito('')
    try {
      await api.del(`/api/estadios/${id}`)
      setExito('Estadio eliminado.')
      cargar()
    } catch (e) { setError(e.message) }
  }

  return (
    <div>
      <h2>Ciudades y Estadios</h2>
      <Mensaje tipo="error" texto={error} />
      <Mensaje tipo="exito" texto={exito} />

      <form className="formulario" onSubmit={crearCiudad}>
        <strong>Nueva ciudad</strong>
        <label>Nombre</label>
        <input required value={formCiudad.nombre} onChange={(e) => setFormCiudad({ ...formCiudad, nombre: e.target.value })} />
        <label>País</label>
        <input required value={formCiudad.pais} onChange={(e) => setFormCiudad({ ...formCiudad, pais: e.target.value })} />
        <button type="submit">Crear ciudad</button>
      </form>

      <form className="formulario" onSubmit={crear}>
        <strong>Nuevo estadio</strong>
        <label>Nombre</label>
        <input required value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
        <label>Ciudad</label>
        <select required value={form.ciudad_id} onChange={(e) => setForm({ ...form, ciudad_id: e.target.value })}>
          <option value="">Selecciona...</option>
          {ciudades.map((c) => <option key={c.id} value={c.id}>{c.nombre}, {c.pais}</option>)}
        </select>
        <label>Capacidad</label>
        <input required type="number" min="1" value={form.capacidad} onChange={(e) => setForm({ ...form, capacidad: e.target.value })} />
        <button type="submit">Crear estadio</button>
      </form>

      <table>
        <thead><tr><th>Nombre</th><th>Ciudad</th><th>Capacidad</th><th>Disponible</th><th></th></tr></thead>
        <tbody>
          {lista.map((e) => (
            <tr key={e.id}>
              <td>{e.nombre}</td>
              <td>{ciudades.find((c) => c.id === e.ciudad_id)?.nombre || '—'}</td>
              <td>{e.capacidad.toLocaleString()}</td>
              <td>{e.disponible ? 'Sí' : 'No'}</td>
              <td><button className="eliminar" onClick={() => eliminar(e.id)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
