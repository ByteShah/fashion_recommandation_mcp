import random
import json

categories = ["kurta", "saree", "lehenga", "shirt", "t-shirt"]
lengths = ["short", "medium", "long"]
fits = ["straight", "a-line", "slim", "relaxed"]
fabrics = ["cotton", "linen", "silk", "rayon", "georgette"]
occasions = ["casual", "office", "party", "wedding", "festive"]
body_types = ["petite", "average", "curvy", "tall"]
colors = ["red", "blue", "ivory", "sage", "black", "gold", "green", "pink"]
sizes = ["XS", "S", "M", "L", "XL", "XXL"]

def generate_mock_item(id):
    return {
        "id": id,
        "category": random.choice(categories),
        "length": random.choice(lengths),
        "fit": random.choice(fits),
        "fabric": random.choice(fabrics),
        "occasion": random.sample(occasions, k=random.randint(1, 3)),
        "suitable_for": random.sample(body_types, k=random.randint(1, 2)),
        "colors": random.sample(colors, k=random.randint(1, 3)),
        "size_range": random.sample(sizes, k=random.randint(1, 4))
    }

fashion_db = [generate_mock_item(i) for i in range(1, 1001)]

# Optional: Save to JSON file
with open("mock_fashion_db.json", "w") as f:
    json.dump(fashion_db, f, indent=2)
