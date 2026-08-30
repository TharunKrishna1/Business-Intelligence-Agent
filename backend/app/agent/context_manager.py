"""Session-based conversation context manager."""

import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    timestamp: Optional[str] = None
    query_plan: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None


class SessionContext(BaseModel):
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)

    def add_user_message(self, text: str):
        self.messages.append(ChatMessage(role="user", content=text))

    def add_assistant_message(
        self, text: str, query_plan: Optional[Dict[str, Any]] = None, metrics: Optional[Dict[str, Any]] = None
    ):
        self.messages.append(
            ChatMessage(role="assistant", content=text, query_plan=query_plan, metrics=metrics)
        )


class ContextManager:
    """In-memory session store (extensible to Redis)."""

    def __init__(self):
        self._sessions: Dict[str, SessionContext] = {}

    def get_or_create_session(self, session_id: Optional[str] = None) -> SessionContext:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionContext(session_id=session_id)

        return self._sessions[session_id]


context_manager = ContextManager()
