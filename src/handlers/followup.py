from typing import Dict
from data.database import fashion_db

async def handle_followup_questions(session_id: str, query: str):
    """
    Handles follow-up questions about specific items or alternative options
    """
    return {
        "session_id": session_id,
        "response": "Here are some alternatives based on your query...",
        "alternatives": fashion_db[:2]  # Mock response
    }