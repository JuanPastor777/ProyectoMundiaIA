const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function manejarRespuesta(resp) {
  const data = await resp.json().catch(() => null)
  if (!resp.ok) {
    const detalle = data?.detail || 'Ocurrió un error al comunicarse con el servidor.'
    throw new Error(typeof detalle === 'string' ? detalle : JSON.stringify(detalle))
  }
  return data
}

async function get(ruta) {
  const resp = await fetch(`${API_URL}${ruta}`)
  return manejarRespuesta(resp)
}

async function post(ruta, body) {
  const resp = await fetch(`${API_URL}${ruta}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return manejarRespuesta(resp)
}

async function put(ruta, body) {
  const resp = await fetch(`${API_URL}${ruta}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return manejarRespuesta(resp)
}

async function del(ruta) {
  const resp = await fetch(`${API_URL}${ruta}`, { method: 'DELETE' })
  return manejarRespuesta(resp)
}

export const api = { get, post, put, del, API_URL }
