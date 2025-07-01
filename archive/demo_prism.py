#!/usr/bin/env python3
"""
Prism AI Voice Assistant Demo
This script demonstrates the Prism voice assistant with mock responses.
"""

import os
import sys
import json
import tempfile
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'prism-secret-key')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class PrismAssistant:
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = """You are Prism, an intelligent and helpful AI voice assistant. 
        You should be conversational, friendly, and provide helpful responses. 
        Keep your responses concise but informative. You can help with:
        - General questions and information
        - Weather updates
        - Setting reminders
        - Playing music
        - Controlling smart home devices
        - Providing news updates
        - Answering questions about various topics
        
        Always respond in a natural, conversational tone."""
    
    def process_query(self, user_input):
        """Process user input and generate mock response"""
        try:
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Generate mock response based on input
            user_input_lower = user_input.lower()
            
            if "hello" in user_input_lower or "hi" in user_input_lower:
                response = "Hello! I'm Prism, your AI voice assistant. How can I help you today?"
            elif "weather" in user_input_lower:
                response = "I'd be happy to help you with weather information! In a real implementation, I would connect to a weather API to get current conditions for your location."
            elif "time" in user_input_lower:
                response = "I can tell you the current time. In a real implementation, I would access your system clock to provide accurate time information."
            elif "music" in user_input_lower or "play" in user_input_lower:
                response = "I can help you play music! In a real implementation, I would connect to your music streaming service to play your favorite songs."
            elif "reminder" in user_input_lower or "remind" in user_input_lower:
                response = "I can set reminders for you. In a real implementation, I would create calendar events or notifications to remind you of important tasks."
            elif "smart home" in user_input_lower or "lights" in user_input_lower:
                response = "I can control your smart home devices! In a real implementation, I would connect to your smart home hub to control lights, thermostats, and other devices."
            elif "news" in user_input_lower:
                response = "I can provide you with the latest news. In a real implementation, I would fetch current news from reliable sources and summarize them for you."
            elif "help" in user_input_lower:
                response = "I'm here to help! I can assist with weather, time, music, reminders, smart home control, news, and general questions. Just ask me anything!"
            else:
                response = f"That's an interesting question about '{user_input}'. In a real implementation, I would use GPT-4o to provide a comprehensive and intelligent response to your query."
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."

# Initialize Prism assistant
prism = PrismAssistant()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages using mock responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process the message through Prism assistant
        response = prism.process_query(user_message)
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Mock text-to-speech endpoint"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Return a mock response indicating TTS would work
        return jsonify({'audio': 'mock_audio_data', 'message': 'TTS would generate audio here'})
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to Prism Demo'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('voice_input')
def handle_voice_input(data):
    """Handle real-time voice input with mock processing"""
    try:
        # Mock voice processing
        emit('transcript', {'text': 'Mock voice input detected'})
        
        # Generate mock response
        assistant_response = prism.process_query("Mock voice input")
        emit('assistant_response', {'text': assistant_response})
        
        # Mock audio response
        emit('audio_response', {'audio': 'mock_audio_data'})
                
    except Exception as e:
        print(f"Error processing voice input: {e}")
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Prism AI Voice Assistant                  ║
    ║                         DEMO MODE                            ║
    ╚══════════════════════════════════════════════════════════════╝
    
    This is a demo version of Prism that works without API keys.
    Features demonstrated:
    - Web interface
    - Text chat with mock responses
    - WebSocket communication
    - Voice input simulation
    
    To use the full version with real AI responses:
    1. Set up your API keys in .env file
    2. Run: python app.py
    
    Demo server starting at: http://localhost:5000
    """)
    
    # Run the application
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 