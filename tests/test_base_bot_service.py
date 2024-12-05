import pytest
from app.services.base import BaseBotService
from app.schemas.message import Message

class TestBaseBotService:
    @pytest.fixture
    def bot_service(self):
        return BaseBotService()

    @pytest.mark.asyncio
    async def test_process_query(self, bot_service):
        # Test basic query processing
        message = Message(content="test message", user_id="test_user")
        with pytest.raises(NotImplementedError):
            await bot_service.process_query(message)

    @pytest.mark.asyncio
    async def test_validate_response(self, bot_service):
        # Test response validation
        response = "test response"
        validated = bot_service.validate_response(response)
        assert validated == response

    def test_is_available(self, bot_service):
        # Test availability check
        assert bot_service.is_available() == True
