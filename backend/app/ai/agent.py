"""
Agente de IA para los organizadores del Mundial 2026.

- Usa la API de OpenAI (function calling).
- Solo puede LEER datos de Supabase a través de las tools en tools.py.
- No tiene acceso a ninguna operación de escritura (insert/update/delete).
"""
import json
from openai import OpenAI
from app.config import settings
from app.ai.tools import TOOLS_OPENAI, FUNCIONES_DISPONIBLES

PROMPT_SISTEMA = """Eres un asistente de inteligencia artificial encargado de apoyar a los organizadores del Mundial FIFA 2026.

Debes responder únicamente consultas relacionadas con el torneo (partidos, selecciones, jugadores, entrenadores, grupos, estadios y estadísticas).

Debes utilizar únicamente la información registrada en el sistema, obtenida mediante las herramientas disponibles. No debes inventar información bajo ninguna circunstancia.

Debes brindar respuestas claras, precisas, amables y profesionales.

Si la información solicitada no existe en la base de datos, debes indicarlo claramente en vez de suponerla.

No puedes modificar, eliminar ni alterar registros: solo puedes consultar y explicar información existente.

No puedes revelar información privada de usuarios del sistema.

Si el usuario pregunta algo que no está relacionado con el Mundial 2026, responde amablemente que solo puedes ayudar con información relacionada con el torneo.
"""

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY no está configurada. Revisa tu archivo backend/.env")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def responder_chat(mensaje_usuario: str) -> str:
    client = _get_client()

    mensajes = [
        {"role": "system", "content": PROMPT_SISTEMA},
        {"role": "user", "content": mensaje_usuario},
    ]

    # Primera llamada: el modelo decide si necesita usar una tool
    respuesta = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=mensajes,
        tools=TOOLS_OPENAI,
        tool_choice="auto",
    )
    mensaje = respuesta.choices[0].message

    # Si el modelo pidió usar una o más tools, las ejecutamos (solo lectura)
    # y le devolvemos el resultado para que redacte la respuesta final.
    if mensaje.tool_calls:
        mensajes.append(mensaje.model_dump(exclude_unset=True))

        for tool_call in mensaje.tool_calls:
            nombre_funcion = tool_call.function.name
            try:
                argumentos = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                argumentos = {}

            funcion = FUNCIONES_DISPONIBLES.get(nombre_funcion)
            if funcion is None:
                resultado = {"error": f"Herramienta desconocida: {nombre_funcion}"}
            else:
                try:
                    resultado = funcion(**argumentos)
                except Exception as e:  # nunca dejar caer el chat por un error de datos
                    resultado = {"error": f"No se pudo completar la consulta: {e}"}

            mensajes.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(resultado, default=str, ensure_ascii=False),
            })

        # Segunda llamada: el modelo redacta la respuesta final con los datos reales
        respuesta_final = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=mensajes,
        )
        return respuesta_final.choices[0].message.content or ""

    return mensaje.content or ""
