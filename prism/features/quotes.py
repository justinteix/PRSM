"""
Quotes service for Prism AI Voice Assistant
Provides inspirational quotes
"""

import random

class QuoteService:
    """Service for inspirational quotes"""
    
    def __init__(self):
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "The best way to predict the future is to invent it. - Alan Kay",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "The journey of a thousand miles begins with one step. - Lao Tzu",
            "Believe you can and you're halfway there. - Theodore Roosevelt"
        ]
    
    def get_quote(self) -> str:
        """Get a random inspirational quote"""
        return random.choice(self.quotes)

# Global instance
quote_service = QuoteService() 