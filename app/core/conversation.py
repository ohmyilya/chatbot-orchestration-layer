from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from app.core.config import settings
import aioredis

class ConversationManager:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)
        self.timeout = timedelta(minutes=settings.CONVERSATION_TIMEOUT_MINUTES)

    async def get_conversation(self, conversation_id: str) -> List[Dict[str, str]]:
        """Retrieve conversation history."""
        try:
            data = await self.redis.get(f"conversation:{conversation_id}")
            if data:
                conversation = json.loads(data)
                if self._is_conversation_expired(conversation):
                    await self.delete_conversation(conversation_id)
                    return []
                return conversation["messages"]
            return []
        except Exception as e:
            print(f"Error retrieving conversation: {str(e)}")
            return []

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Add a message to the conversation history."""
        try:
            data = await self.redis.get(f"conversation:{conversation_id}")
            if data:
                conversation = json.loads(data)
                messages = conversation["messages"]
            else:
                conversation = {
                    "created_at": datetime.utcnow().isoformat(),
                    "messages": []
                }
                messages = conversation["messages"]

            # Add new message
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            }
            if metadata:
                message["metadata"] = metadata

            messages.append(message)

            # Trim conversation history if needed
            if len(messages) > settings.MAX_CONVERSATION_HISTORY:
                messages = messages[-settings.MAX_CONVERSATION_HISTORY:]

            conversation["messages"] = messages
            conversation["updated_at"] = datetime.utcnow().isoformat()

            # Save to Redis with expiration
            await self.redis.setex(
                f"conversation:{conversation_id}",
                self.timeout,
                json.dumps(conversation)
            )
            return True
        except Exception as e:
            print(f"Error adding message: {str(e)}")
            return False

    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        try:
            await self.redis.delete(f"conversation:{conversation_id}")
            return True
        except Exception as e:
            print(f"Error deleting conversation: {str(e)}")
            return False

    def _is_conversation_expired(self, conversation: Dict) -> bool:
        """Check if a conversation has expired."""
        updated_at = datetime.fromisoformat(conversation.get("updated_at", conversation["created_at"]))
        return datetime.utcnow() - updated_at > self.timeout

    async def get_active_conversations(self) -> List[str]:
        """Get a list of active conversation IDs."""
        try:
            keys = await self.redis.keys("conversation:*")
            return [key.split(":")[1] for key in keys]
        except Exception as e:
            print(f"Error getting active conversations: {str(e)}")
            return []

    async def get_conversation_metadata(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation metadata."""
        try:
            data = await self.redis.get(f"conversation:{conversation_id}")
            if data:
                conversation = json.loads(data)
                return {
                    "created_at": conversation["created_at"],
                    "updated_at": conversation.get("updated_at"),
                    "message_count": len(conversation["messages"]),
                    "is_expired": self._is_conversation_expired(conversation)
                }
            return None
        except Exception as e:
            print(f"Error getting conversation metadata: {str(e)}")
            return None
