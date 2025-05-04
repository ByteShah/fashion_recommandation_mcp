from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from typing import Dict, Any
import uuid
import sys
import json

load_dotenv()

# Add debug logging
print("Starting Fashion MCP server...", file=sys.stderr)
mcp = FastMCP("fashion")
print("FastMCP instance created", file=sys.stderr)

# Load Fashion Database from JSON file
with open("mock_fashion_db.json", "r") as f:
    fashion_db = json.load(f)

sessions: Dict[str, Dict[str, Any]] = {}

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

@mcp.tool()
async def initiate_fashion_assistant(user_query: str):
    """
    Starts fashion recommendation conversation flow.
    Ask clarifying questions to understand user needs.
    """
    session_id = SessionManager.create_session()
    
    return {
        "session_id": session_id,
        "next_questions": [
            "What type of clothing are you looking for? (e.g., kurta, dress, lehenga)",
            "What's the occasion? (e.g., wedding, casual, office)"
        ],
        "message": "Welcome to Fashion Assistant! Let's find your perfect outfit."
    }

@mcp.tool()
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

@mcp.tool()
async def generate_recommendations(session_id: str):
    """
    Generates personalized recommendations based on collected preferences
    """
    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session"}
    
    prefs = session["preferences"]
    
    # Filter recommendations
    recommendations = []
    for item in fashion_db:
        match = True
        
        # Category matching
        if prefs.get("category") and item["category"] != prefs["category"]:
            continue
            
        # Body type compatibility
        if prefs.get("body_type") and prefs["body_type"] not in item["suitable_for"]:
            continue
            
        # Occasion filtering
        if prefs.get("occasion") and prefs["occasion"] not in item["occasion"]:
            continue
            
        # Length preference
        if prefs.get("length") and item["length"] != prefs["length"]:
            continue
            
        recommendations.append(item)
    
    # Sort by relevance (add scoring logic here)
    sorted_recs = sorted(
        recommendations,
        key=lambda x: len(set(x.values()) & set(prefs.values())),
        reverse=True
    )[:5]  # Return top 5
    
    # Prepare response
    response = {
        "session_id": session_id,
        "recommendations": sorted_recs,
        "preferences_used": prefs,
        "message": f"Based on your preferences, here are {len(sorted_recs)} recommendations:"
    }
    
    # Add complementary items suggestion
    if sorted_recs:
        response["complementary_suggestions"] = get_complementary_items(sorted_recs[0])
    
    return response

def get_complementary_items(main_item: Dict) -> Dict:
    """
    Suggest complementary items based on selected piece
    """
    # Implement matching logic for accessories/bottomwear/etc
    return {
        "matching_bottoms": ["palazzo pants", "leggings"],
        "accessories": ["statement necklace", "juttis"],
        "shawls": ["linen stole", "embroidered dupatta"]
    }

@mcp.tool()
async def handle_followup_questions(session_id: str, query: str):
    """
    Handles follow-up questions about specific items or alternative options
    """
    # Implement NLP-based query handling or use embeddings for similarity search
    return {
        "session_id": session_id,
        "response": "Here are some alternatives based on your query...",
        "alternatives": fashion_db[:2]  # Mock response
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")