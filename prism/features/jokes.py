"""
Jokes service for Prism AI Voice Assistant
Provides random jokes and humor
"""

import random

class JokeService:
    """Service for jokes and humor"""
    
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fish wearing a bowtie? So-fish-ticated!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "What do you call a can opener that doesn't work? A can't opener!"
        ]
    
    def get_joke(self) -> str:
        """Get a random joke"""
        return random.choice(self.jokes)

# Global instance
joke_service = JokeService() 