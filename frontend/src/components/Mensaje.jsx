export default function Mensaje({ tipo, texto }) {
  if (!texto) return null
  const clase = tipo === 'error' ? 'mensaje-error' : 'mensaje-exito'
  return <div className={clase}>{texto}</div>
}
