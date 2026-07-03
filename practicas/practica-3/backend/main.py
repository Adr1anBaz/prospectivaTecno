import time
from typing import List, Dict, Optional

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


app = FastAPI(
    title="Chatbot LLM local con Ollama y contexto (SQLite)",
    description="API intermedia para conversar con modelos locales mediante Ollama, con historial persistente en SQLite.",
    version="2.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[int] = Field(
        default=None, description="ID de la conversación (None para iniciar una nueva)"
    )
    model: str = Field(default="llama3.2:3b", min_length=1)

    temperature: float = Field(default=0.7, ge=0.0, le=1.2)
    top_p: float = Field(default=0.9, ge=0.1, le=1.0)
    num_predict: int = Field(default=160, ge=20, le=1000)
    num_ctx: int = Field(default=4096, ge=512, le=8192)
    repeat_penalty: float = Field(default=1.1, ge=1.0, le=2.0)

    keep_alive: str = Field(default="5m")
    system_prompt: str = Field(
        default="Eres un asistente académico claro, preciso y útil para estudiantes universitarios."
    )


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
    model: str
    created_at: str
    updated_at: str
    message_count: int


class ConversationDetailResponse(BaseModel):
    id: int
    title: str
    model: str
    created_at: str
    updated_at: str
    messages: List[MessageResponse]


@app.get("/")
def root():
    return {
        "message": "API de chatbot local con Ollama y contexto (SQLite)",
        "docs": "/docs",
        "health": "/health",
        "conversations": "/conversations",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


def build_messages_with_history(
    system_prompt: str, history: list, user_message: str
) -> List[Dict[str, str]]:
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        if msg.role != "system":
            messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_message})
    return messages


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if request.conversation_id is None:
        conversation = create_conversation(db, title="Nueva conversación", model=request.model)
    else:
        conversation = get_conversation(db, request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")

    conversation_id = conversation.id

    history = get_conversation_messages(db, conversation_id)
    messages = build_messages_with_history(request.system_prompt, history, request.message)

    add_message(db, conversation_id, "user", request.message)

    payload = {
        "model": request.model,
        "messages": messages,
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

    total_duration_s = data.get("total_duration", 0) / 1e9
    load_duration_s = data.get("load_duration", 0) / 1e9
    prompt_eval_count = data.get("prompt_eval_count", 0)
    eval_count = data.get("eval_count", 0)
    eval_duration_s = data.get("eval_duration", 0) / 1e9

    total_tokens = prompt_eval_count + eval_count
    tokens_per_second = eval_count / eval_duration_s if eval_duration_s > 0 else 0

    add_message(db, conversation_id, "assistant", reply)

    if len(history) == 0:
        title = request.message[:50] + ("..." if len(request.message) > 50 else "")
        update_conversation_title(db, conversation_id, title)

    return ChatResponse(
        conversation_id=conversation_id,
        model=request.model,
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
    conversations = get_all_conversations(db)
    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            model=conv.model,
            created_at=conv.created_at.isoformat(),
            updated_at=conv.updated_at.isoformat(),
            message_count=len(conv.messages),
        )
        for conv in conversations
    ]


@app.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation_detail(conversation_id: int, db: Session = Depends(get_db)):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        model=conversation.model,
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
    success = delete_conversation(db, conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return {"message": "Conversación eliminada exitosamente"}
