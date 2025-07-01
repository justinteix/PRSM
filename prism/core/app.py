"""
Flask application factory for Prism AI Voice Assistant
"""

import os
import json
import base64
import tempfile
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import openai
from dotenv import load_dotenv
import wave
import io
from typing import Dict, Any, List, Optional
import re
import requests

from .assistant import PrismAssistant
from ..features.weather import weather_service
from ..features.news import news_service
from ..features.reminders import reminder_service
from ..features.calculator import calculator_service
from ..features.jokes import joke_service
from ..features.quotes import quote_service

# Load environment variables from config directory
load_dotenv('config/.env')

def create_app():
    """Create and configure the Flask application"""
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prism_dir = os.path.dirname(current_dir)  # Go up to prism directory
    
    app = Flask(__name__, 
                template_folder=os.path.join(prism_dir, 'templates'),
                static_folder=os.path.join(prism_dir, 'static'))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'prism-secret-key')
    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize API clients
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    # Initialize Prism assistant
    prism = PrismAssistant()
    
    @app.route('/')
    def index():
        """Serve the main application page"""
        return render_template('index.html')
    
    @app.route('/api/speech-to-text', methods=['POST'])
    def speech_to_text():
        """Convert speech to text using Google Cloud Speech-to-Text"""
        try:
            # Get audio data from request
            audio_data = request.files.get('audio')
            if not audio_data:
                print("❌ No audio data provided")
                return jsonify({'error': 'No audio data provided'}), 400
            
            print(f"📁 Received audio file: {audio_data.filename}, size: {len(audio_data.read())} bytes")
            audio_data.seek(0)  # Reset file pointer
            
            # Save audio to temporary file
            temp_file_path = None
            try:
                # Get the original filename to check format
                original_filename = audio_data.filename or 'audio'
                print(f"📁 Original filename: {original_filename}")
                
                # Determine the correct file extension
                if '.' in original_filename:
                    file_ext = original_filename.split('.')[-1].lower()
                else:
                    file_ext = 'wav'  # Default to wav
                
                # Use the original extension if it's supported by Google Cloud Speech
                supported_formats = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']
                if file_ext not in supported_formats:
                    file_ext = 'wav'  # Fallback to wav
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}') as temp_file:
                    audio_data.save(temp_file.name)
                    temp_file_path = temp_file.name
                    print(f"💾 Saved audio to: {temp_file_path} (format: {file_ext})")
                
                # Use Google Cloud Speech-to-Text for speech recognition
                try:
                    from google.cloud import speech
                    
                    # Initialize the client
                    client = speech.SpeechClient()
                    
                    # Read the audio file
                    with open(temp_file_path, 'rb') as audio_file:
                        content = audio_file.read()
                    
                    # Configure the recognition
                    audio = speech.RecognitionAudio(content=content)
                    config = speech.RecognitionConfig(
                        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                        language_code="en-US",
                        enable_automatic_punctuation=True,
                    )
                    
                    print("🎤 Sending to Google Cloud Speech-to-Text API...")
                    response = client.recognize(config=config, audio=audio)
                    
                    # Extract the transcript
                    transcript = ""
                    for result in response.results:
                        transcript += result.alternatives[0].transcript
                    
                    print(f"✅ Google Cloud Speech response: '{transcript}'")
                    return jsonify({'transcript': transcript})
                    
                except Exception as e:
                    print(f"❌ Error in Google Cloud Speech transcription: {e}")
                    return jsonify({'error': str(e)}), 500
                finally:
                    # Clean up temporary file
                    if temp_file_path and os.path.exists(temp_file_path):
                        try:
                            os.unlink(temp_file_path)
                            print("🗑️  Cleaned up temp file")
                        except Exception as e:
                            print(f"⚠️  Warning: Could not delete temp file {temp_file_path}: {e}")
                            
            except Exception as e:
                print(f"❌ Error saving audio file: {e}")
                return jsonify({'error': 'Error processing audio file'}), 500
                
        except Exception as e:
            print(f"❌ Error in speech-to-text: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/text-to-speech', methods=['POST'])
    def text_to_speech():
        """Convert text to speech using ElevenLabs TTS with debug logging"""
        try:
            import requests
            data = request.get_json()
            text = data.get('text', '')
            if not text:
                print("No text provided")
                return jsonify({'error': 'No text provided'}), 400

            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                print("No ElevenLabs API key set")
                return jsonify({'error': 'ElevenLabs API key not set'}), 500

            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice ID - more reliable
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(url, headers=headers, json=payload)
            print(f"ElevenLabs API status: {response.status_code}")
            if response.status_code != 200:
                print("ElevenLabs API error response:", response.text)
                return jsonify({'error': 'ElevenLabs TTS failed', 'details': response.text}), 500

            audio_content = response.content
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            return jsonify({'audio': audio_base64})

        except Exception as e:
            import traceback
            print("Exception in ElevenLabs TTS:", traceback.format_exc())
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Process chat messages using GPT-4o"""
        try:
            data = request.get_json()
            user_message = data.get('message', '')
            lat = data.get('lat')
            lon = data.get('lon')
            
            if not user_message:
                return jsonify({'error': 'No message provided'}), 400
            
            # Process the message through Prism assistant
            response = prism.process_query(user_message, lat=lat, lon=lon)
            
            return jsonify({'response': response})
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/weather', methods=['GET'])
    def get_weather():
        """Get weather information"""
        try:
            lat = request.args.get('lat')
            lon = request.args.get('lon')
            location = request.args.get('location', 'auto')
            if lat and lon:
                weather = weather_service.get_weather_by_coords(lat, lon)
            else:
                weather = weather_service.get_weather(location)
            return jsonify({
                'location': weather.location,
                'temperature': weather.temperature,
                'condition': weather.condition,
                'humidity': weather.humidity,
                'wind_speed': weather.wind_speed,
                'forecast': weather.forecast
            })
        except Exception as e:
            print(f"Error getting weather: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/news', methods=['GET'])
    def get_news():
        """Get latest news"""
        try:
            category = request.args.get('category', 'general')
            limit = int(request.args.get('limit', 5))
            
            news_items = news_service.get_news(category, limit)
            
            return jsonify({
                'articles': [
                    {
                        'title': item.title,
                        'description': item.description,
                        'url': item.url,
                        'source': item.source,
                        'published_at': item.published_at
                    }
                    for item in news_items
                ]
            })
            
        except Exception as e:
            print(f"Error getting news: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/reminders', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def manage_reminders():
        """Manage reminders"""
        try:
            if request.method == 'GET':
                # Get all reminders
                include_completed = request.args.get('include_completed', 'false').lower() == 'true'
                reminders = reminder_service.get_reminders(include_completed)
                
                return jsonify({
                    'reminders': [
                        {
                            'id': reminder.id,
                            'title': reminder.title,
                            'datetime': reminder.datetime.isoformat(),
                            'completed': reminder.completed
                        }
                        for reminder in reminders
                    ]
                })
                
            elif request.method == 'POST':
                # Create new reminder
                data = request.get_json()
                title = data.get('title')
                time_str = data.get('time')
                
                if not title or not time_str:
                    return jsonify({'error': 'Title and time are required'}), 400
                
                reminder = reminder_service.add_reminder(title, time_str)
                
                return jsonify({
                    'id': reminder.id,
                    'title': reminder.title,
                    'datetime': reminder.datetime.isoformat(),
                    'completed': reminder.completed
                }), 201
                
            elif request.method == 'PUT':
                # Complete a reminder
                data = request.get_json()
                reminder_id = data.get('id')
                action = data.get('action')
                
                if not reminder_id:
                    return jsonify({'error': 'Reminder ID is required'}), 400
                
                if action == 'complete':
                    success = reminder_service.complete_reminder(reminder_id)
                    if success:
                        return jsonify({'message': 'Reminder completed'})
                    else:
                        return jsonify({'error': 'Reminder not found'}), 404
                
            elif request.method == 'DELETE':
                # Delete a reminder
                reminder_id = request.args.get('id')
                
                if not reminder_id:
                    return jsonify({'error': 'Reminder ID is required'}), 400
                
                success = reminder_service.delete_reminder(reminder_id)
                if success:
                    return jsonify({'message': 'Reminder deleted'})
                else:
                    return jsonify({'error': 'Reminder not found'}), 404
                    
        except Exception as e:
            print(f"Error managing reminders: {e}")
            return jsonify({'error': str(e)}), 500
        
        # Default return for unhandled cases
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.route('/api/time', methods=['GET'])
    def get_time():
        """Get current time and date"""
        try:
            from datetime import datetime
            now = datetime.now()
            # Format time without leading zeros for better TTS pronunciation
            hour = now.strftime("%I").lstrip("0")  # Remove leading zero from hour
            minute = now.strftime("%M")
            ampm = now.strftime("%p")
            day = now.strftime("%A")
            month = now.strftime("%B")
            day_num = now.strftime("%d").lstrip("0")  # Remove leading zero from day
            year = now.strftime("%Y")
            
            current_time = f"{hour}:{minute} {ampm} on {day}, {month} {day_num}, {year}"
            return jsonify({'time': current_time})
            
        except Exception as e:
            print(f"Error getting time: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/calculate', methods=['POST'])
    def calculate():
        """Perform calculations"""
        try:
            data = request.get_json()
            expression = data.get('expression', '')
            
            if not expression:
                return jsonify({'error': 'Expression is required'}), 400
            
            result = calculator_service.calculate(expression)
            return jsonify({'result': result})
            
        except Exception as e:
            print(f"Error calculating: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/joke', methods=['GET'])
    def get_joke():
        """Get a random joke"""
        try:
            joke = joke_service.get_joke()
            return jsonify({'joke': joke})
            
        except Exception as e:
            print(f"Error getting joke: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/quote', methods=['GET'])
    def get_quote():
        """Get an inspirational quote"""
        try:
            quote = quote_service.get_quote()
            return jsonify({'quote': quote})
            
        except Exception as e:
            print(f"Error getting quote: {e}")
            return jsonify({'error': str(e)}), 500
    
    @socketio.on('connect')
    def handle_connect():
        """Handle WebSocket connection"""
        print('Client connected')
        emit('status', {'message': 'Connected to Prism'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle WebSocket disconnection"""
        print('Client disconnected')
    
    @socketio.on('voice_input')
    def handle_voice_input(data):
        """Handle real-time voice input"""
        try:
            # Process the voice input
            audio_data = data.get('audio')
            if audio_data:
                print(f"🎤 Received WebSocket audio data, length: {len(audio_data)}")
                
                # Check if the data URL is valid
                if not audio_data.startswith('data:'):
                    print("❌ Invalid audio data format - not a data URL")
                    emit('error', {'message': 'Invalid audio data format'})
                    return
                
                # Extract the MIME type and base64 data
                try:
                    header, base64_data = audio_data.split(',', 1)
                    mime_type = header.split(':')[1].split(';')[0]
                    print(f"📊 MIME type: {mime_type}")
                    print(f"📊 Base64 data length: {len(base64_data)}")
                except Exception as e:
                    print(f"❌ Error parsing data URL: {e}")
                    emit('error', {'message': 'Error parsing audio data'})
                    return
                
                # Convert base64 audio to bytes
                try:
                    audio_bytes = base64.b64decode(base64_data)
                    print(f"📊 Decoded audio bytes: {len(audio_bytes)} bytes")
                    
                    if len(audio_bytes) == 0:
                        print("❌ No audio data after decoding")
                        emit('error', {'message': 'No audio data received'})
                        return
                        
                except Exception as e:
                    print(f"❌ Error decoding base64: {e}")
                    emit('error', {'message': 'Error decoding audio data'})
                    return
                
                # Save to temporary file as WAV (Google Cloud's most reliable format)
                temp_file_path = None
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                        temp_file.write(audio_bytes)
                        temp_file_path = temp_file.name
                        print(f"💾 Saved audio as WAV: {temp_file_path}")
                        print(f"💾 File size: {os.path.getsize(temp_file_path)} bytes")
                    
                    # Use Google Cloud Speech-to-Text for speech recognition
                    try:
                        from google.cloud import speech
                        
                        # Initialize the client
                        client = speech.SpeechClient()
                        
                        # Read the audio file
                        with open(temp_file_path, 'rb') as audio_file:
                            content = audio_file.read()
                        
                        print(f"📖 Read {len(content)} bytes from temp file")
                        
                        # Configure the recognition
                        audio = speech.RecognitionAudio(content=content)
                        config = speech.RecognitionConfig(
                            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                            language_code="en-US",
                            enable_automatic_punctuation=True,
                        )
                        
                        print("🎤 Sending to Google Cloud Speech-to-Text API...")
                        response = client.recognize(config=config, audio=audio)
                        
                        # Extract the transcript
                        transcript = ""
                        for result in response.results:
                            transcript += result.alternatives[0].transcript
                        
                        print(f"✅ Google Cloud Speech response: '{transcript}'")
                        emit('transcript', {'text': transcript})
                        
                        # Process with GPT-4o
                        assistant_response = prism.process_query(transcript)
                        emit('assistant_response', {'text': assistant_response})
                        
                        # Generate speech response using ElevenLabs TTS (same as text-to-speech endpoint)
                        try:
                            import requests
                            api_key = os.getenv('ELEVENLABS_API_KEY')
                            if not api_key:
                                print("No ElevenLabs API key set")
                                emit('error', {'message': 'ElevenLabs API key not set'})
                                return

                            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice ID - same as text-to-speech endpoint
                            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

                            headers = {
                                "xi-api-key": api_key,
                                "Content-Type": "application/json"
                            }
                            payload = {
                                "text": assistant_response,
                                "voice_settings": {
                                    "stability": 0.5,
                                    "similarity_boost": 0.75
                                }
                            }

                            response = requests.post(url, headers=headers, json=payload)
                            print(f"ElevenLabs API status: {response.status_code}")
                            if response.status_code != 200:
                                print("ElevenLabs API error response:", response.text)
                                emit('error', {'message': 'ElevenLabs TTS failed'})
                                return

                            audio_content = response.content
                            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
                            emit('audio_response', {'audio': audio_base64})
                            
                        except Exception as e:
                            print(f"Error generating speech: {e}")
                            emit('error', {'message': 'Error generating speech response'})
                            
                    except Exception as e:
                        print(f"Error in Google Cloud Speech transcription: {e}")
                        emit('error', {'message': 'Error transcribing audio'})
                    finally:
                        # Clean up temporary file
                        if temp_file_path and os.path.exists(temp_file_path):
                            try:
                                os.unlink(temp_file_path)
                                print("🗑️  Cleaned up temp file")
                            except Exception as e:
                                print(f"⚠️  Warning: Could not delete temp file {temp_file_path}: {e}")
                                
                except Exception as e:
                    print(f"Error saving audio file: {e}")
                    emit('error', {'message': 'Error processing audio file'})
            else:
                print("❌ No audio data received in WebSocket")
                emit('error', {'message': 'No audio data received'})
                    
        except Exception as e:
            print(f"Error processing voice input: {e}")
            emit('error', {'message': str(e)})
    
    return app, socketio 