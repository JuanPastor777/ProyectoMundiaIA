from fastapi import APIRouter, HTTPException
from app.schemas.otros import ChatRequest, ChatResponse
from app.ai.agent import responder_chat

router = APIRouter(prefix="/api/ai", tags=["Agente IA"])


@router.post("/chat", response_model=ChatResponse)
def chat(datos: ChatRequest):
    if not datos.mensaje or not datos.mensaje.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")
    try:
        respuesta = responder_chat(datos.mensaje)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ChatResponse(respuesta=respuesta)
