# Chatbot Orchestration Layer

A powerful meta-layer for orchestrating multiple chatbots and AI services, enabling seamless integration and coordination of various AI models and services. This platform provides intelligent routing, load balancing, and unified management of multiple AI interactions.

## Features

- **Intelligent Query Routing**: Automatically directs queries to the most appropriate bot service
- **Multi-Model Support**: Integration with various AI models (GPT, LLAMA, Custom Models)
- **Advanced Orchestration**:
  - Load balancing and failover mechanisms
  - Conversation history management
  - Context preservation across services
- **Monitoring & Analytics**:
  - Real-time performance monitoring
  - Usage analytics and insights
  - Cost tracking per service
- **Security Features**:
  - Rate limiting
  - Authentication and authorization
  - API key management
- **Easy Integration**:
  - RESTful API interface
  - WebSocket support for real-time communication
  - Plug-and-play bot service integration

## Tech Stack

- **Backend**: Python 3.8+ with FastAPI
- **Database**: PostgreSQL for persistent storage
- **Caching**: Redis for session management and caching
- **Message Queue**: Redis for message queuing
- **Container**: Docker and Docker Compose
- **AI Integration**: Support for various AI models via standardized interfaces

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL 13+
- Redis 6+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ohmyilya/chatbot-orchestration-layer.git
cd chatbot-orchestration-layer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your orchestration layer configuration
```

5. Start the services using Docker Compose:
```bash
docker-compose up -d
```

6. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Project Structure

```
chatbot-orchestration-layer/
├── app/
│   ├── api/            # API routes and endpoints
│   │   ├── v1/        # API version 1
│   │   └── websocket/ # WebSocket handlers
│   ├── core/          # Core orchestration logic
│   │   ├── router.py  # Query routing logic
│   │   ├── manager.py # Service management
│   │   └── auth.py    # Authentication
│   ├── models/        # Data models and schemas
│   ├── services/      # Bot service integrations
│   │   ├── gpt/      # GPT service integration
│   │   └── llama/    # LLAMA model integration
│   └── utils/         # Utility functions
├── tests/             # Test suite
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── docker/           # Docker configuration
└── docs/            # Documentation
```

## API Documentation

Once the service is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

The service can be configured using environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `MODEL_CONFIGS`: AI model configurations
- `MAX_REQUESTS_PER_MIN`: Rate limiting configuration
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your PR:
- Includes tests for new functionality
- Updates documentation as needed
- Follows the existing code style
- Includes a clear description of changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@ohmyilya](https://github.com/ohmyilya)

Project Link: [https://github.com/ohmyilya/chatbot-orchestration-layer](https://github.com/ohmyilya/chatbot-orchestration-layer)
