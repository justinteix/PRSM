# Prism AI Voice Assistant - Project Structure

## 📁 Directory Organization

```
Prism.ai/
├── 📁 config/                    # Configuration files
│   ├── .env                      # Environment variables
│   └── google-cloud-key.json     # Google Cloud credentials
│
├── 📁 prism/                     # Main application package
│   ├── 📁 api/                   # API endpoints
│   ├── 📁 core/                  # Core application logic
│   │   ├── app.py               # Flask application factory
│   │   └── assistant.py         # Main assistant class
│   ├── 📁 features/              # Feature modules
│   │   ├── calculator.py        # Calculator service
│   │   ├── jokes.py             # Jokes service
│   │   ├── news.py              # News service
│   │   ├── quotes.py            # Quotes service
│   │   ├── reminders.py         # Reminders service
│   │   ├── search.py            # Search service
│   │   └── weather.py           # Weather service
│   ├── 📁 static/                # Static assets (CSS, JS, images)
│   ├── 📁 templates/             # HTML templates
│   └── 📁 utils/                 # Utility functions
│
├── 📁 docs/                      # Documentation
│   ├── env_example.txt          # Environment variables template
│   ├── google_cloud_setup.md    # Google Cloud setup guide
│   ├── README_REFACTORED.md     # Refactored README
│   └── CLEANUP_SUMMARY.md       # Cleanup documentation
│
├── 📁 tools/                     # Development and testing tools
│   └── test_elevenlabs.py       # ElevenLabs API testing
│
├── 📁 scripts/                   # Utility scripts
│   ├── run_prism.bat            # Windows startup script
│   ├── run_prism.sh             # Linux/Mac startup script
│   └── setup_features.py        # Feature setup script
│
├── 📁 tests/                     # Test files
│   └── test_features.py         # Feature tests
│
├── 📁 archive/                   # Legacy/archived files
│   ├── prism_features.py        # Old features implementation
│   ├── test_*.py                # Old test files
│   └── demo_prism.py            # Old demo files
│
├── 📁 .venv/                     # Virtual environment (gitignored)
├── main.py                       # Main application entry point
├── app.py                        # Legacy entry point (deprecated)
├── requirements.txt              # Python dependencies
├── setup.py                      # Setup script
├── README.md                     # Main project README
├── .gitignore                    # Git ignore rules
└── PROJECT_STRUCTURE.md          # This file
```

## 🚀 Quick Start

### Running the Application
```bash
# Using the new main entry point
python main.py

# Or using the scripts
./scripts/run_prism.sh    # Linux/Mac
scripts/run_prism.bat     # Windows
```

### Configuration
1. Copy `docs/env_example.txt` to `config/.env`
2. Add your API keys to `config/.env`
3. Place your Google Cloud credentials in `config/google-cloud-key.json`

## 📋 Key Files

- **`main.py`**: New main entry point with proper configuration loading
- **`prism/core/app.py`**: Flask application factory and routes
- **`prism/core/assistant.py`**: Main AI assistant logic
- **`config/.env`**: Environment variables and API keys
- **`requirements.txt`**: Python package dependencies

## 🔧 Development

### Adding New Features
1. Create new service in `prism/features/`
2. Add routes in `prism/core/app.py`
3. Integrate with assistant in `prism/core/assistant.py`

### Testing
- Use `tools/test_elevenlabs.py` to test ElevenLabs API
- Run `tests/test_features.py` for feature testing

### Configuration Management
- All configuration files are in `config/` directory
- Environment variables loaded from `config/.env`
- Credentials stored in `config/` directory

## 📚 Documentation

- **`README.md`**: Main project documentation
- **`docs/`**: Detailed guides and examples
- **`PROJECT_STRUCTURE.md`**: This file - project organization

## 🗂️ Archive

The `archive/` directory contains legacy files that are no longer used but kept for reference:
- Old feature implementations
- Previous test files
- Demo applications
- Deprecated scripts 