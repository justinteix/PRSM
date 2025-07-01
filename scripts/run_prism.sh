#!/bin/bash

echo ""
echo "========================================"
echo "    Prism AI Voice Assistant"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "Python version: $python_version"

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import flask, openai, elevenlabs" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f config/.env ]; then
    echo "Creating .env file from template..."
    mkdir -p config
    cp docs/env_example.txt config/.env
    echo ""
    echo "Please edit the config/.env file and add your API keys before running again."
    echo ""
    exit 1
fi

# Run the application
echo "Starting Prism..."
echo ""
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the application"
echo ""
python3 main.py 