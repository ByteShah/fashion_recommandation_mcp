import uuid
from typing import Dict, Any
from .store import sessions

class SessionManager:
    @staticmethod
    def create_session() -> str:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "step": "start",
            "preferences": {},
            "previous_answers": {},
            "context": {}
        }
        return session_id

    @staticmethod
    def update_step(session_id: str, step: str):
        sessions[session_id]["step"] = step

    @staticmethod
    def add_preference(session_id: str, key: str, value: Any):
        sessions[session_id]["preferences"][key] = value