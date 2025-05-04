from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import sys
from data.database import load_fashion_db
from handlers.assistant import register_assistant_handlers

load_dotenv()

# Add debug logging
print("Starting Fashion MCP server...", file=sys.stderr)
mcp = FastMCP("fashion")
print("FastMCP instance created", file=sys.stderr)

# Initialize database and handlers
load_fashion_db()
register_assistant_handlers(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")