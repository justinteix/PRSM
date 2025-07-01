# Prism AI Voice Assistant - Refactored Structure

A comprehensive AI-powered voice home assistant built with Python Flask, featuring modular architecture and multiple AI services.

## 🏗️ Project Structure

```
Prism.ai/
│
├── app_new.py                    # New main application entry point
├── app.py                        # Original app (legacy)
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── .env                          # Environment variables (not in git)
├── README.md                     # Original documentation
├── README_REFACTORED.md          # This file
│
├── prism/                        # Main application package
│   ├── __init__.py              # Package initialization
│   ├── core/                    # Core application components
│   │   ├── __init__.py
│   │   ├── assistant.py         # PrismAssistant class
│   │   └── app.py              # Flask app factory
│   ├── features/                # Feature modules
│   │   ├── __init__.py
│   │   ├── weather.py          # Weather service
│   │   ├── news.py             # News service
│   │   ├── reminders.py        # Reminder management
│   │   ├── calculator.py       # Calculator service
│   │   ├── jokes.py            # Joke service
│   │   ├── quotes.py           # Quote service
│   │   └── search.py           # Search service
│   ├── utils/                   # Utility functions
│   │   └── __init__.py
│   ├── api/                     # API endpoints
│   │   └── __init__.py
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/               # HTML templates
│       └── index.html
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_features.py
│   ├── test_api.py
│   └── test_assistant.py
│
├── docs/                         # Documentation
│   ├── setup.md
│   ├── api.md
│   └── deployment.md
│
├── scripts/                      # Utility scripts
│   ├── setup_features.py
│   ├── test_features.py
│   └── run_tests.py
│
└── legacy/                       # Legacy files (to be cleaned up)
    ├── prism_features.py
    ├── demo_prism.py
    └── other_old_files.py
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Optional (for enhanced features)
OPENWEATHER_API_KEY=your_openweather_api_key_here
NEWS_API_KEY=your_news_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. Run the Application

**New Refactored Version:**
```bash
python app_new.py
```

**Legacy Version:**
```bash
python app.py
```

### 4. Access the Web Interface

Open your browser and navigate to: http://localhost:5000

## 🏛️ Architecture Overview

### Core Components

- **`prism/core/assistant.py`**: Main AI assistant class that handles conversation and feature integration
- **`prism/core/app.py`**: Flask application factory that creates and configures the web application
- **`prism/features/`**: Modular feature services for different capabilities

### Feature Services

Each feature is implemented as a separate service class:

- **WeatherService**: Provides weather information using OpenWeatherMap API
- **NewsService**: Fetches news articles using NewsAPI
- **ReminderService**: Manages reminders with natural language parsing
- **CalculatorService**: Performs mathematical calculations
- **JokeService**: Provides random jokes and humor
- **QuoteService**: Offers inspirational quotes
- **SearchService**: Simulates web search functionality

### Benefits of the New Structure

1. **Modularity**: Each feature is self-contained and can be easily modified or extended
2. **Testability**: Individual components can be tested in isolation
3. **Maintainability**: Clear separation of concerns makes the code easier to understand and maintain
4. **Scalability**: New features can be added by creating new service modules
5. **Reusability**: Services can be used independently or in combination

## 🔧 Development

### Adding New Features

1. Create a new service in `prism/features/`
2. Add the service to `prism/features/__init__.py`
3. Import and use the service in `prism/core/assistant.py`
4. Add API endpoints in `prism/core/app.py` if needed

### Example: Adding a Timer Service

```python
# prism/features/timer.py
class TimerService:
    def start_timer(self, duration: int) -> str:
        return f"Timer started for {duration} seconds"

# prism/features/__init__.py
from .timer import TimerService

# prism/core/assistant.py
from ..features.timer import timer_service

# Add to _handle_feature_requests method
elif any(word in user_input_lower for word in ['timer', 'countdown']):
    return timer_service.start_timer(60)
```

### Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual tests:

```bash
python tests/test_features.py
```

## 📚 API Documentation

### Core Endpoints

- `GET /`: Main web interface
- `POST /api/chat`: Process text messages
- `POST /api/speech-to-text`: Convert speech to text
- `POST /api/text-to-speech`: Convert text to speech

### Feature Endpoints

- `GET /api/weather`: Get weather information
- `GET /api/news`: Get latest news
- `GET /api/time`: Get current time
- `POST /api/calculate`: Perform calculations
- `GET /api/joke`: Get a random joke
- `GET /api/quote`: Get an inspirational quote
- `GET/POST/PUT/DELETE /api/reminders`: Manage reminders

### WebSocket Events

- `connect`: Client connection
- `disconnect`: Client disconnection
- `voice_input`: Real-time voice processing

## 🚀 Deployment

### Local Development

```bash
python app_new.py
```

### Production Deployment

1. Set up a production WSGI server (Gunicorn, uWSGI)
2. Configure environment variables
3. Set up reverse proxy (Nginx)
4. Enable HTTPS

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "prism.core.app:create_app()"
```

## 🔄 Migration from Legacy Structure

The refactored structure maintains backward compatibility. To migrate:

1. **Immediate**: Use `app_new.py` instead of `app.py`
2. **Gradual**: Move remaining files to appropriate directories
3. **Cleanup**: Remove legacy files once migration is complete

### File Mapping

| Legacy File | New Location |
|-------------|--------------|
| `prism_features.py` | `prism/features/` (split into modules) |
| `app.py` | `prism/core/app.py` (app factory) |
| `templates/` | `prism/templates/` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the modular structure for new features
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation in `docs/`
2. Review existing issues
3. Create a new issue with detailed information

---

**Note**: This refactored structure provides a solid foundation for future development while maintaining all existing functionality. The modular approach makes it easier to add new features, fix bugs, and maintain the codebase. 