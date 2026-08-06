import { useState } from 'react'
import { api } from '../services/api'
import Mensaje from '../components/Mensaje'

export default function Asistente() {
  const [historial, setHistorial] = useState([])
  const [mensaje, setMensaje] = useState('')
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  async function enviar(e) {
    e.preventDefault()
    if (!mensaje.trim()) return
    setError('')
    const nuevoHistorial = [...historial, { rol: 'usuario', texto: mensaje }]
    setHistorial(nuevoHistorial)
    setMensaje('')
    setCargando(true)
    try {
      const resp = await api.post('/api/ai/chat', { mensaje })
      setHistorial([...nuevoHistorial, { rol: 'ia', texto: resp.respuesta }])
    } catch (e) {
      setError(e.message)
    } finally {
      setCargando(false)
    }
  }

  return (
    <div>
      <h2>Asistente IA del Mundial 2026</h2>
      <p>Pregunta sobre partidos, selecciones, jugadores, estadios o estadísticas del torneo.</p>
      <Mensaje tipo="error" texto={error} />

      <div className="chat-caja">
        <div className="chat-historial">
          {historial.length === 0 && <p style={{ color: '#777' }}>Ejemplo: "¿Cuándo juega Argentina?" o "Genera un reporte del Grupo A"</p>}
          {historial.map((m, i) => (
            <div key={i} className={`chat-msg ${m.rol}`}>
              <div className="burbuja">{m.texto}</div>
            </div>
          ))}
          {cargando && <div className="chat-msg ia"><div className="burbuja">Consultando...</div></div>}
        </div>
        <form onSubmit={enviar} style={{ display: 'flex', gap: '0.5rem' }}>
          <input
            style={{ flex: 1, padding: '0.5rem', border: '1px solid #dde3ea', borderRadius: '4px' }}
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
            placeholder="Escribe tu pregunta..."
          />
          <button type="submit" disabled={cargando}>Enviar</button>
        </form>
      </div>
    </div>
  )
}
