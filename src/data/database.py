import json
from typing import List, Dict, Any
import os
import json

fashion_db: List[Dict[str, Any]] = []

# Color groupings for flexible matching
COLOR_GROUPS = {
    "pastel": ["sage", "ivory", "pink"],
    "bright": ["red", "gold", "blue"],
    "neutral": ["black", "ivory"],
    "warm": ["red", "gold"],
    "cool": ["blue", "sage"]
}

def load_fashion_db():
    global fashion_db
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "mock_fashion_db.json")
    with open(db_path, "r") as f:
        fashion_db = json.load(f)

def find_matching_colors(color_preference: str) -> List[str]:
    """Find matching colors based on preference"""
    if color_preference in COLOR_GROUPS:
        return COLOR_GROUPS[color_preference]
    return [color_preference]  # Return exact match if no group found