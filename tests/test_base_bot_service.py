import pytest
from unittest.mock import AsyncMock, patch
from app.services.base import BaseBotService
from app.schemas.message import Message

class TestBaseBotService:
    @pytest.fixture
    def bot_service(self):
        return BaseBotService()

    @pytest.mark.asyncio
    async def test_process_query_not_implemented(self, bot_service):
        # Test that process_query raises NotImplementedError
        message = Message(content="test message", user_id="test_user")
        with pytest.raises(NotImplementedError):
            await bot_service.process_query(message)

    def test_validate_response_valid(self, bot_service):
        # Test valid response validation
        response = "test response"
        validated = bot_service.validate_response(response)
        assert validated == response

    def test_validate_response_empty(self, bot_service):
        # Test empty response validation
        response = ""
        with pytest.raises(ValueError, match="Response cannot be empty"):
            bot_service.validate_response(response)

    def test_validate_response_none(self, bot_service):
        # Test None response validation
        with pytest.raises(ValueError, match="Response cannot be None"):
            bot_service.validate_response(None)

    def test_is_available(self, bot_service):
        # Test availability check
        assert bot_service.is_available() == True

    @pytest.mark.asyncio
    async def test_process_query_mock(self):
        # Mock implementation to test query processing
        class MockBotService(BaseBotService):
            async def process_query(self, message):
                return f"Processed: {message.content}"

        mock_service = MockBotService()
        message = Message(content="test query", user_id="mock_user")
        result = await mock_service.process_query(message)
        assert result == "Processed: test query"
