import json
from datetime import datetime
from typing import Dict, List, Any


def format_message(sender: str, message: str) -> Dict[str, Any]:
    """Format a message with sender information and timestamp."""
    return {
        'sender': sender,
        'content': message,
        'timestamp': datetime.now().isoformat()
    }


def save_conversation(conversation: List[Dict[str, Any]], file_path: str) -> bool:
    """Save the conversation to a JSON file.
    
    Args:
        conversation: List of message dictionaries
        file_path: Path to save the JSON file
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(conversation, f, indent=2)
        return True
    except Exception:
        return False


def load_conversation(file_path: str) -> List[Dict[str, Any]]:
    """Load a conversation from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        List of message dictionaries
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception:
        return [] 