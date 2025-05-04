from typing import Dict
from session.manager import SessionManager
from .recommendations import generate_recommendations

async def handle_user_response(session_id: str, answers: Dict[str, str]):
    """
    Processes user answers and determines next questions.
    Maintains conversation context for personalized recommendations.
    """
    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session"}
    
    # Update preferences with received answers
    for key, value in answers.items():
        SessionManager.add_preference(session_id, key, value)
    
    # Determine next questions based on current step
    next_questions = []
    if session["step"] == "start":
        next_questions = [
            "What's your preferred length? (short/medium/long)",
            "Do you have any specific fabric preference? (cotton/silk/linen)"
        ]
        SessionManager.update_step(session_id, "body_info")
    elif session["step"] == "body_info":
        next_questions = [
            "What's your body type? (petite/curvy/athletic)",
            "What's your height range? (under 5'2/5'3-5'6/over 5'7)"
        ]
        SessionManager.update_step(session_id, "style_prefs")
    elif session["step"] == "style_prefs":
        next_questions = [
            "Preferred color palette? (neutral/bright/pastel)",
            "Any specific pattern preferences? (solid/printed/embroidered)"
        ]
        SessionManager.update_step(session_id, "finalize")
    else:
        return await generate_recommendations(session_id)
    
    return {
        "session_id": session_id,
        "next_questions": next_questions,
        "context": session["preferences"]
    }