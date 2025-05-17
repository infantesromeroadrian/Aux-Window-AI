from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class Message:
    """Represents a single message in a conversation."""
    sender: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary representation."""
        return {
            'sender': self.sender,
            'content': self.content,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create a Message instance from a dictionary."""
        return cls(
            sender=data['sender'],
            content=data['content'],
            timestamp=data.get('timestamp', datetime.now().isoformat())
        )


@dataclass
class Conversation:
    """Represents a conversation between an agent and a client."""
    id: str
    messages: List[Message] = field(default_factory=list)
    
    def add_message(self, sender: str, content: str) -> Message:
        """Add a new message to the conversation.
        
        Args:
            sender: The sender of the message (agent or client)
            content: The content of the message
            
        Returns:
            The created Message object
        """
        message = Message(sender=sender, content=content)
        self.messages.append(message)
        return message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary representation."""
        return {
            'id': self.id,
            'messages': [msg.to_dict() for msg in self.messages]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """Create a Conversation instance from a dictionary."""
        conversation = cls(id=data['id'])
        conversation.messages = [
            Message.from_dict(msg) for msg in data.get('messages', [])
        ]
        return conversation 