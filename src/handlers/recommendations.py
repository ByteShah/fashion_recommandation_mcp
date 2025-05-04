from typing import Dict
from session.store import sessions
from data.database import fashion_db
from .complementary import get_complementary_items

from typing import Dict, List
from data.database import fashion_db, find_matching_colors

def calculate_match_score(item: Dict, prefs: Dict) -> float:
    score = 0.0
    
    # Category match (highest priority)
    if prefs.get("category") and item["category"] == prefs["category"]:
        score += 3.0
    
    # Color preference matching
    if prefs.get("color_palette"):
        matching_colors = find_matching_colors(prefs["color_palette"])
        if any(color in item["colors"] for color in matching_colors):
            score += 2.0
    
    # Occasion matching
    if prefs.get("occasion") and prefs["occasion"] in item["occasion"]:
        score += 1.5
    
    # Body type matching
    if prefs.get("body_type") and prefs["body_type"] in item["suitable_for"]:
        score += 1.0
    
    return score

async def generate_recommendations(session_id: str):
    """
    Generates personalized recommendations with flexible matching
    """
    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session"}
    
    prefs = session["preferences"]
    
    # Score and sort all items
    scored_items = [
        (item, calculate_match_score(item, prefs))
        for item in fashion_db
    ]
    
    # Sort by score and get top matches
    recommendations = [
        item for item, score in sorted(
            scored_items, 
            key=lambda x: x[1], 
            reverse=True
        ) if score > 0
    ][:5]
    
    # Generate follow-up questions based on missing preferences
    follow_up = []
    if recommendations and not prefs.get("body_type"):
        follow_up.append("Would you like to filter by body type for better recommendations?")
    
    response = {
        "session_id": session_id,
        "recommendations": recommendations,
        "preferences_used": prefs,
        "message": f"Found {len(recommendations)} items that match your style!",
        "follow_up_questions": follow_up if follow_up else None
    }
    
    return response