"""
Prism AI Voice Assistant
A comprehensive AI-powered voice home assistant with multiple features.
"""

__version__ = "1.0.0"
__author__ = "Prism AI Team"

from .core.assistant import PrismAssistant
from .core.app import create_app

__all__ = ['PrismAssistant', 'create_app'] 