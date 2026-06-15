import time
from typing import Optional, List, Dict

import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import (
    get_db,
    create_conversation,
    get_conversation,
    get_all_conversations,
    add_message,
    get_conversation_messages,
    delete_conversation,
    update_conversation_title,
)


OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"


# Copilot profiles with predefined system prompts
COPILOT_PROFILES: Dict[str, Dict[str, str]] = {
    "generico": {
        "label": "Asistente genérico",
        "system_prompt": (
            "Eres un asistente académico claro, preciso y útil para estudiantes universitarios. "
            "Respondes de forma ordenada, honesta y con lenguaje comprensible."
        ),
    },
    "docente": {
        "label": "Copiloto docente universitario",
        "system_prompt": (
            "Eres un copiloto docente universitario. Ayudas a diseñar clases, actividades, rúbricas, "
            "objetivos de aprendizaje y explicaciones para estudiantes. Respondes con tono académico claro. "
            "Cuando diseñes una actividad, incluye objetivo, duración, materiales, pasos y criterios de evaluación. "
            "Si falta información sobre nivel, duración o materia, pregunta antes de asumir."
        ),
    },
    "robotica": {
        "label": "Copiloto de robótica móvil",
        "system_prompt": (
            "Eres un copiloto de robótica móvil educativa. Ayudas a estudiantes universitarios a comprender sensores, "
            "actuadores, cinemática, control, comunicación y programación de robots. Respondes con lenguaje técnico claro, "
            "ejemplos prácticos y advertencias de seguridad. Cuando la pregunta involucre conexiones eléctricas, motores, "
            "baterías o drivers, debes pedir datos faltantes como voltaje, corriente, modelo de componente y diagrama de conexión "
            "antes de dar instrucciones específicas."
        ),
    },
    "programacion": {
        "label": "Copiloto de programación Python",
        "system_prompt": (
            "Eres un copiloto de programación en Python para estudiantes universitarios. Explicas paso a paso, propones código claro, "
            "comentado y reproducible. Si el usuario muestra un error, primero interpreta el mensaje, luego propone una causa probable "
            "y finalmente da una corrección verificable. No inventes funciones ni librerías inexistentes."
        ),
    },
    "investigacion": {
        "label": "Copiloto de investigación académica",
        "system_prompt": (
            "Eres un copiloto de investigación académica. Ayudas a formular preguntas de investigación, organizar argumentos, "
            "estructurar marcos teóricos y detectar vacíos conceptuales. Debes separar hechos, inferencias y recomendaciones. "
            "No inventes citas, autores, DOI ni resultados. Si no tienes una fuente verificable, dilo explícitamente."
        ),
    },
}


app = FastAPI(
    title="Chatbot LLM local con Ollama",
    description="API intermedia para conversar con modelos locales mediante Ollama con historial persistente.",
    version="2.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[int] = Field(default=None, description="ID de la conversación (None para nueva)")
    model: str = Field(default="llama3.2:3b", min_length=1, max_length=100)

    copilot_profile: str = Field(default="generico", min_length=1, max_length=50)
    system_prompt: str = Field(default="", max_length=6000)

    temperature: float = Field(default=0.7, ge=0.0, le=1.2)
    top_p: float = Field(default=0.9, ge=0.1, le=1.0)
    num_predict: int = Field(default=800, ge=20, le=4000)
    num_ctx: int = Field(default=4096, ge=512, le=8192)
    repeat_penalty: float = Field(default=1.1, ge=1.0, le=2.0)

    keep_alive: str = Field(default="5m", max_length=20)


class ChatMetrics(BaseModel):
    wall_time_s: float
    total_duration_s: float
    load_duration_s: float
    prompt_eval_count: int
    eval_count: int
    total_tokens: int
    eval_duration_s: float
    tokens_per_second: float


class ChatResponse(BaseModel):
    conversation_id: int
    model: str
    copilot_profile: str
    copilot_label: str
    system_prompt_used: str
    reply: str
    metrics: ChatMetrics


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str


class ConversationResponse(BaseModel):
    id: int
    title: str
    copilot_profile: str
    model: str
    created_at: str
    updated_at: str
    message_count: int


class ConversationDetailResponse(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str
    messages: List[MessageResponse]


@app.get("/")
def root():
    return {
        "message": "API de chatbot local con Ollama con historial persistente",
        "docs": "/docs",
        "health": "/health",
        "version": "2.0.0",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/profiles")
def get_profiles():
    """Get all available copilot profiles"""
    return COPILOT_PROFILES


def get_profile(profile_id: str) -> Dict[str, str]:
    """Get a profile by ID, raise exception if not found"""
    if profile_id not in COPILOT_PROFILES:
        raise HTTPException(
            status_code=400,
            detail=f"Perfil no válido: {profile_id}. Usa GET /profiles para ver perfiles disponibles.",
        )
    return COPILOT_PROFILES[profile_id]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the chatbot.
    If conversation_id is None, creates a new conversation.
    Otherwise, continues the existing conversation.
    """

    # Get profile and determine system prompt to use
    profile = get_profile(request.copilot_profile)

    system_prompt_used = request.system_prompt.strip()
    if not system_prompt_used:
        system_prompt_used = profile["system_prompt"]

    # Get or create conversation
    if request.conversation_id is None:
        # Create new conversation with profile information
        conversation = create_conversation(
            db,
            title="Nueva conversación",
            copilot_profile=request.copilot_profile,
            model=request.model
        )
        conversation_id = conversation.id
    else:
        # Use existing conversation
        conversation = get_conversation(db, request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        conversation_id = conversation.id

    # Get conversation history
    messages = get_conversation_messages(db, conversation_id)

    # Build message history for Ollama
    message_history = []

    # Add system prompt
    message_history.append({
        "role": "system",
        "content": system_prompt_used,
    })

    # Add previous messages from database
    for msg in messages:
        if msg.role != "system":  # Don't duplicate system messages
            message_history.append({
                "role": msg.role,
                "content": msg.content,
            })

    # Add current user message
    message_history.append({
        "role": "user",
        "content": request.message,
    })

    # Save user message to database
    add_message(db, conversation_id, "user", request.message)

    # Prepare payload for Ollama
    payload = {
        "model": request.model,
        "messages": message_history,
        "stream": False,
        "keep_alive": request.keep_alive,
        "options": {
            "temperature": request.temperature,
            "top_p": request.top_p,
            "num_predict": request.num_predict,
            "num_ctx": request.num_ctx,
            "repeat_penalty": request.repeat_penalty,
        },
    }

    try:
        start_time = time.perf_counter()
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=300)
        end_time = time.perf_counter()

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con Ollama. Verifica que Ollama esté ejecutándose.",
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise HTTPException(
            status_code=504,
            detail="La solicitud a Ollama tardó demasiado tiempo.",
        ) from exc

    except requests.exceptions.HTTPError as exc:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error devuelto por Ollama: {response.text}",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(exc)}",
        ) from exc

    message = data.get("message", {})
    reply = message.get("content", "")

    # Save assistant reply to database
    add_message(db, conversation_id, "assistant", reply)

    # Update conversation title if it's the first exchange
    if len(messages) == 0:
        # Generate a short title from the first user message
        title = request.message[:50] + ("..." if len(request.message) > 50 else "")
        update_conversation_title(db, conversation_id, title)

    # Extract metrics
    total_duration_s = data.get("total_duration", 0) / 1e9
    load_duration_s = data.get("load_duration", 0) / 1e9
    prompt_eval_count = data.get("prompt_eval_count", 0)
    eval_count = data.get("eval_count", 0)
    eval_duration_s = data.get("eval_duration", 0) / 1e9

    total_tokens = prompt_eval_count + eval_count
    tokens_per_second = eval_count / eval_duration_s if eval_duration_s > 0 else 0

    return ChatResponse(
        conversation_id=conversation_id,
        model=request.model,
        copilot_profile=request.copilot_profile,
        copilot_label=profile["label"],
        system_prompt_used=system_prompt_used,
        reply=reply,
        metrics=ChatMetrics(
            wall_time_s=end_time - start_time,
            total_duration_s=total_duration_s,
            load_duration_s=load_duration_s,
            prompt_eval_count=prompt_eval_count,
            eval_count=eval_count,
            total_tokens=total_tokens,
            eval_duration_s=eval_duration_s,
            tokens_per_second=tokens_per_second,
        ),
    )


@app.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(db: Session = Depends(get_db)):
    """Get all conversations"""
    conversations = get_all_conversations(db)
    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            copilot_profile=conv.copilot_profile,
            model=conv.model,
            created_at=conv.created_at.isoformat(),
            updated_at=conv.updated_at.isoformat(),
            message_count=len(conv.messages),
        )
        for conv in conversations
    ]


@app.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation_detail(conversation_id: int, db: Session = Depends(get_db)):
    """Get a specific conversation with all its messages"""
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat(),
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat(),
            )
            for msg in conversation.messages
        ],
    )


@app.delete("/conversations/{conversation_id}")
def remove_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Delete a conversation and all its messages"""
    success = delete_conversation(db, conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return {"message": "Conversación eliminada exitosamente"}


class CreateConversationRequest(BaseModel):
    title: str = Field(default="Nueva conversación", max_length=200)
    copilot_profile: str = Field(default="generico", max_length=50)
    model: str = Field(default="llama3.2:3b", max_length=100)


@app.post("/conversations", response_model=ConversationResponse)
def create_new_conversation(request: CreateConversationRequest, db: Session = Depends(get_db)):
    """Create a new empty conversation"""
    conversation = create_conversation(
        db,
        title=request.title,
        copilot_profile=request.copilot_profile,
        model=request.model
    )
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        copilot_profile=conversation.copilot_profile,
        model=conversation.model,
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat(),
        message_count=0,
    )
