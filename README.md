# Prism AI Voice Assistant

Prism is an intelligent AI-powered voice home assistant built with Python Flask, featuring real-time voice interaction, natural language processing, and a comprehensive set of home assistant capabilities.

## 🌟 Features

### Core Voice Assistant
- **Real-time Voice Recognition**: Powered by Google Cloud Speech-to-Text
- **Natural Language Processing**: GPT-4o-mini for intelligent conversations
- **Text-to-Speech**: OpenAI TTS for natural voice responses
- **WebSocket Support**: Real-time bidirectional communication
- **Cross-platform**: Works on desktop and mobile browsers

### Home Assistant Capabilities

#### 🌤️ Weather Information
- Current weather conditions
- Temperature, humidity, wind speed
- 5-day weather forecast
- Location-based weather (auto-detect or specify location)
- Voice commands: "What's the weather like?", "Weather in New York"

#### 📰 News Updates
- Latest headlines from multiple categories
- Technology, world news, science, and more
- Configurable news sources
- Voice commands: "What's the latest news?", "Tell me the headlines"

#### ⏰ Smart Reminders
- Natural language reminder creation
- Flexible time parsing ("tomorrow at 3pm", "in 2 hours", "next Monday")
- Reminder management (complete, delete, list)
- Voice commands: "Remind me to call mom tomorrow at 3pm"

#### 🧮 Calculator
- Mathematical calculations
- Natural language math expressions
- Support for basic operations (+, -, *, /)
- Voice commands: "What is 15 plus 27?", "Calculate 100 divided by 4"

#### 🕐 Time & Date
- Current time and date
- Formatted time display
- Voice commands: "What time is it?", "Current time"

#### 😄 Entertainment
- Random jokes and humor
- Inspirational quotes
- Voice commands: "Tell me a joke", "Give me a quote"

#### 🔍 Web Search
- Simulated web search functionality
- Information lookup
- Voice commands: "Search for Python tutorials", "What is machine learning?"

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud account (for Speech-to-Text)
- OpenAI API key (for GPT and TTS)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Prism.ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json
   OPENWEATHER_API_KEY=your_openweather_api_key_here  # Optional
   NEWS_API_KEY=your_news_api_key_here  # Optional
   ```

4. **Set up Google Cloud Speech-to-Text**
   - Create a Google Cloud project
   - Enable the Speech-to-Text API
   - Create a service account and download the JSON credentials
   - Set the path in your `.env` file

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 Voice Commands

### Weather
- "What's the weather like?"
- "Weather in [location]"
- "What's the temperature?"
- "Is it going to rain?"

### News
- "What's the latest news?"
- "Tell me the headlines"
- "What's happening in the world?"
- "Technology news"

### Reminders
- "Remind me to [task] [time]"
- "Set a reminder for [task] tomorrow at [time]"
- "Remind me to call mom in 2 hours"
- "Remind me to buy groceries next Monday at 5pm"

### Time & Date
- "What time is it?"
- "Current time"
- "What's today's date?"

### Calculator
- "What is [number] plus [number]?"
- "Calculate [expression]"
- "What's 15 times 7?"
- "100 divided by 4"

### Entertainment
- "Tell me a joke"
- "Make me laugh"
- "Give me an inspirational quote"
- "Motivational quote"

### General
- "Hello"
- "How are you?"
- "What can you do?"
- "Help"

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Main application interface
- `POST /api/speech-to-text` - Convert audio to text
- `POST /api/text-to-speech` - Convert text to speech
- `POST /api/chat` - Process chat messages

### Feature Endpoints
- `GET /api/weather?location=[location]` - Get weather information
- `GET /api/news?category=[category]&limit=[number]` - Get latest news
- `GET /api/time` - Get current time
- `POST /api/calculate` - Perform calculations
- `GET /api/joke` - Get a random joke
- `GET /api/quote` - Get an inspirational quote

### Reminder Management
- `GET /api/reminders` - List all reminders
- `POST /api/reminders` - Create new reminder
- `PUT /api/reminders` - Complete a reminder
- `DELETE /api/reminders?id=[id]` - Delete a reminder

## 🛠️ Configuration

### Optional API Keys
For enhanced functionality, you can add these optional API keys:

#### OpenWeather API
- Get real weather data instead of mock data
- Sign up at [OpenWeather](https://openweathermap.org/api)
- Add to `.env`: `OPENWEATHER_API_KEY=your_key_here`

#### News API
- Get real news headlines instead of mock data
- Sign up at [NewsAPI](https://newsapi.org/)
- Add to `.env`: `NEWS_API_KEY=your_key_here`

### Environment Variables
```env
# Required
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Optional
OPENWEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_news_api_key
SECRET_KEY=your_secret_key
```

## 🏗️ Architecture

### Backend Components
- **Flask**: Web framework and API server
- **Socket.IO**: Real-time WebSocket communication
- **Google Cloud Speech-to-Text**: Voice recognition
- **OpenAI GPT-4o-mini**: Natural language processing
- **OpenAI TTS**: Text-to-speech synthesis
- **PrismFeatures**: Home assistant capabilities module

### Frontend Components
- **HTML5 Audio API**: Audio capture and playback
- **Web Audio API**: Audio processing and conversion
- **Socket.IO Client**: Real-time communication
- **Responsive Design**: Mobile-friendly interface

## 🔍 Troubleshooting

### Common Issues

1. **"No audio data captured"**
   - Check microphone permissions
   - Try refreshing the page
   - Ensure HTTPS in production

2. **"Google Cloud credentials not found"**
   - Verify the path in `GOOGLE_APPLICATION_CREDENTIALS`
   - Ensure the service account has Speech-to-Text permissions

3. **"OpenAI API error"**
   - Check your API key is valid
   - Verify you have sufficient credits
   - Check API rate limits

4. **Audio format issues**
   - The app automatically converts audio to WAV format
   - Ensure your browser supports Web Audio API

### Debug Mode
Run with debug logging:
```bash
python app.py
```
Check the console for detailed error messages and API responses.

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT and TTS APIs
- Google Cloud for Speech-to-Text
- Flask and Socket.IO communities
- OpenWeather and NewsAPI for data services

---

**Prism AI Voice Assistant** - Your intelligent home companion! 🏠✨ 