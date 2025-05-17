import os
import json
import uuid
from typing import List, Dict, Any, Optional

from models.conversation import Conversation, Message


class ConversationService:
    """Service for managing conversations."""
    
    def __init__(self, storage_dir: str = 'data/conversations'):
        """Initialize the conversation service.
        
        Args:
            storage_dir: Directory where conversations will be stored
        """
        self._storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def create_conversation(self) -> Conversation:
        """Create a new conversation.
        
        Returns:
            A new Conversation instance
        """
        conversation_id = str(uuid.uuid4())
        return Conversation(id=conversation_id)
    
    def add_message(self, conversation_id: str, sender: str, content: str) -> Optional[Message]:
        """Add a message to an existing conversation.
        
        Args:
            conversation_id: ID of the conversation
            sender: Sender of the message
            content: Content of the message
            
        Returns:
            The created Message or None if conversation not found
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return None
        
        message = conversation.add_message(sender, content)
        self._save_conversation(conversation)
        return message
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID.
        
        Args:
            conversation_id: ID of the conversation to retrieve
            
        Returns:
            The Conversation if found, None otherwise
        """
        file_path = self._get_conversation_file_path(conversation_id)
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return Conversation.from_dict(data)
        except Exception:
            return None
    
    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all available conversations.
        
        Returns:
            List of conversation summaries
        """
        conversations = []
        
        if not os.path.exists(self._storage_dir):
            return conversations
            
        for filename in os.listdir(self._storage_dir):
            if filename.endswith('.json'):
                conversation_id = filename.replace('.json', '')
                try:
                    conversation = self.get_conversation(conversation_id)
                    if conversation:
                        messages_count = len(conversation.messages)
                        last_message = None
                        if messages_count > 0:
                            last_message = conversation.messages[-1].to_dict()
                            
                        conversations.append({
                            'id': conversation_id,
                            'messages_count': messages_count,
                            'last_message': last_message
                        })
                except Exception:
                    pass
                    
        return conversations
    
    def _get_conversation_file_path(self, conversation_id: str) -> str:
        """Get the file path for a conversation.
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Path to the conversation's JSON file
        """
        return os.path.join(self._storage_dir, f"{conversation_id}.json")
    
    def _save_conversation(self, conversation: Conversation) -> bool:
        """Save a conversation to disk.
        
        Args:
            conversation: The conversation to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        file_path = self._get_conversation_file_path(conversation.id)
        try:
            with open(file_path, 'w') as f:
                json.dump(conversation.to_dict(), f, indent=2)
            return True
        except Exception:
            return False 