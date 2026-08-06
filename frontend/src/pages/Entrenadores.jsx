import { useEffect, useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

const VACIO = { nombre: '', apellido: '', nacionalidad: '' }

export default function Entrenadores() {
  const [lista, setLista] = useState([])
  const [form, setForm] = useState(VACIO)
  const [error, setError] = useState('')
  const [exito, setExito] = useState('')

  function cargar() {
    api.get('/api/entrenadores').then(setLista).catch((e) => setError(e.message))
  }
  useEffect(cargar, [])

  async function crear(e) {
    e.preventDefault()
    setError(''); setExito('')
    try {
      await api.post('/api/entrenadores', form)
      setExito('Entrenador creado.')
      setForm(VACIO)
      cargar()
    } catch (e) { setError(e.message) }
  }

  async function eliminar(id) {
    setError(''); setExito('')
    try {
      await api.del(`/api/entrenadores/${id}`)
      setExito('Entrenador eliminado.')
      cargar()
    } catch (e) { setError(e.message) }
  }

  return (
    <div>
      <h2>Entrenadores</h2>
      <Mensaje tipo="error" texto={error} />
      <Mensaje tipo="exito" texto={exito} />

      <form className="formulario" onSubmit={crear}>
        <label>Nombre</label>
        <input required value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
        <label>Apellido</label>
        <input required value={form.apellido} onChange={(e) => setForm({ ...form, apellido: e.target.value })} />
        <label>Nacionalidad</label>
        <input value={form.nacionalidad} onChange={(e) => setForm({ ...form, nacionalidad: e.target.value })} />
        <button type="submit">Crear entrenador</button>
      </form>

      <table>
        <thead><tr><th>Nombre</th><th>Nacionalidad</th><th></th></tr></thead>
        <tbody>
          {lista.map((en) => (
            <tr key={en.id}>
              <td>{en.nombre} {en.apellido}</td>
              <td>{en.nacionalidad || '—'}</td>
              <td><button className="eliminar" onClick={() => eliminar(en.id)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
