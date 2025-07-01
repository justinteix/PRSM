"""
Search service for Prism AI Voice Assistant
Provides web search simulation
"""

import re

class SearchService:
    """Service for web search simulation"""
    
    def __init__(self):
        self.search_results = {
            "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
            "ai": "Artificial Intelligence (AI) is the simulation of human intelligence in machines.",
            "machine learning": "Machine Learning is a subset of AI that enables computers to learn without being explicitly programmed.",
            "flask": "Flask is a lightweight web framework for Python that's easy to use and flexible.",
            "openai": "OpenAI is an AI research company that develops advanced language models like GPT.",
            "weather": "Weather refers to the state of the atmosphere at a particular place and time.",
            "news": "News is information about recent events or developments.",
            "calculator": "A calculator is a device used for performing mathematical calculations.",
            "reminder": "A reminder is a note or notification to help you remember something important."
        }
    
    def search_web(self, query: str) -> str:
        """Simulate web search results"""
        query = query.lower().strip()
        
        # Remove common search words
        query = re.sub(r'\b(search|find|look up|what is|tell me about)\b', '', query, flags=re.IGNORECASE)
        query = query.strip()
        
        # Check if we have a predefined result
        for key, result in self.search_results.items():
            if key in query:
                return f"Here's what I found about '{query}': {result}"
        
        # Generic response for unknown queries
        return f"I found several results about '{query}'. Here are some key points: This topic covers various aspects and has been widely discussed in recent years. For more detailed information, you might want to search online or ask me a more specific question."
    
    def add_search_result(self, keyword: str, result: str):
        """Add a new search result"""
        self.search_results[keyword.lower()] = result

# Global instance
search_service = SearchService() 