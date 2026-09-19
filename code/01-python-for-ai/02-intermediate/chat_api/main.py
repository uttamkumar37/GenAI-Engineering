from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI

from .models import ChatRequest, ChatResponse
from .settings import Settings, get_settings

app = FastAPI(title="chat_api")


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    settings: Annotated[Settings, Depends(get_settings)],
) -> ChatResponse:
    reply = f"[{settings.provider_name}] echo: {request.message}"
    tokens_used = min(len(reply.split()), settings.max_reply_tokens)
    return ChatResponse(reply=reply, user_id=request.user_id, tokens_used=tokens_used)
