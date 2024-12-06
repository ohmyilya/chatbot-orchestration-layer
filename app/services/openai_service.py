from typing import List, Dict, Optional
import httpx
from app.core.config import settings
from app.services.base import BaseService

class OpenAIService(BaseService):
    def __init__(self):
        super().__init__()
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.model = settings.DEFAULT_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def validate_api_key(self) -> bool:
        """Validate the OpenAI API key."""
        if not self.api_key:
            return False
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                return response.status_code == 200
        except Exception:
            return False

    async def process_message(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> str:
        """Process a message using OpenAI's API."""
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        if conversation_history is None:
            conversation_history = []

        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        
        # Add conversation history
        for msg in conversation_history[-settings.MAX_CONVERSATION_HISTORY:]:
            messages.append({
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })
        
        # Add the current message
        messages.append({"role": "user", "content": message})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": settings.MAX_TOKENS,
                        "temperature": settings.TEMPERATURE,
                    },
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"OpenAI API error: {response.text}")
                
                result = response.json()
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            raise Exception(f"Error processing message with OpenAI: {str(e)}")

    async def get_available_models(self) -> List[str]:
        """Get a list of available OpenAI models."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                if response.status_code != 200:
                    raise Exception(f"OpenAI API error: {response.text}")
                
                models = response.json()["data"]
                return [model["id"] for model in models]
        except Exception as e:
            raise Exception(f"Error fetching OpenAI models: {str(e)}")
