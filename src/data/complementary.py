from typing import Dict

def get_complementary_items(main_item: Dict) -> Dict:
    """
    Suggest complementary items based on selected piece
    """
    return {
        "matching_bottoms": ["palazzo pants", "leggings"],
        "accessories": ["statement necklace", "juttis"],
        "shawls": ["linen stole", "embroidered dupatta"]
    }