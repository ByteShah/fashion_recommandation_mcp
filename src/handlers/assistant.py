from mcp.server.fastmcp import FastMCP
from session.manager import SessionManager
from handlers.recommendations import generate_recommendations
from handlers.response import handle_user_response
from handlers.followup import handle_followup_questions

def register_assistant_handlers(mcp: FastMCP):
    @mcp.tool()
    async def initiate_fashion_assistant(user_query: str):
        """
        Starts fashion recommendation flow with minimal questions
        """
        session_id = SessionManager.create_session()
        
        # Extract category from query if possible
        categories = ["kurta", "lehenga", "saree", "dress"]
        initial_category = next((cat for cat in categories if cat in user_query.lower()), None)
        
        if initial_category:
            SessionManager.add_preference(session_id, "category", initial_category)
            return {
                "session_id": session_id,
                "next_questions": ["What's the occasion? (casual/festive/party/wedding)"],
                "message": f"Great choice! Let's find you the perfect {initial_category}."
            }
        
        return {
            "session_id": session_id,
            "next_questions": ["What type of clothing are you looking for?"],
            "message": "Welcome! Let's find your perfect outfit."
        }

    mcp.tool()(handle_user_response)
    mcp.tool()(generate_recommendations)
    mcp.tool()(handle_followup_questions)