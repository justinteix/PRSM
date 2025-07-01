"""
News service for Prism AI Voice Assistant
Provides news information using NewsAPI
"""

import os
import requests
import re
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()

@dataclass
class NewsItem:
    """News item data structure"""
    title: str
    description: str
    url: str
    source: str
    published_at: str

class NewsService:
    """Service for news-related operations"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
    
    def _make_tts_friendly(self, text: str) -> str:
        """Convert text to be more natural for Text-to-Speech"""
        if not text:
            return text
        
        # Convert to string if needed
        text = str(text)
        
        # Remove common source attributions that NewsAPI adds to headlines
        source_patterns = [
            r'\s*-\s*[A-Za-z\s&\.]+$',  # " - Source Name" (including dots and ampersands)
            r'\s*—\s*[A-Za-z\s&\.]+$',  # " — Source Name"
            r'\s*–\s*[A-Za-z\s&\.]+$',  # " – Source Name"
            r'\s*\|[A-Za-z\s&\.]+$',    # " | Source Name"
            r'\s*•\s*[A-Za-z\s&\.]+$',  # " • Source Name"
            r'\s*via\s+[A-Za-z\s&\.]+$', # " via Source Name"
            r'\s*by\s+[A-Za-z\s&\.]+$',  # " by Source Name"
            r'\s*\([A-Za-z\s&\.]+\)$',   # " (Source Name)"
            r'\s*\[[A-Za-z\s&\.]+\]$',   # " [Source Name]"
            r'\s*Source:\s*[A-Za-z\s&\.]+$', # "Source: Source Name"
            r'\s*From\s+[A-Za-z\s&\.]+$', # "From Source Name"
            # Handle complex source attributions like "ABC News - Breaking News, Latest News and Videos"
            r'\s*-\s*[A-Za-z\s&\.]+(?:\s*-\s*[A-Za-z\s&,]+)*$',  # Multiple dash-separated parts
            r'\s*-\s*[A-Za-z\s&\.]+(?:\s*,\s*[A-Za-z\s&]+)*$',   # Comma-separated parts
        ]
        
        # More aggressive pattern to catch any source-like text at the end
        # This looks for common source indicators followed by capitalized words
        aggressive_patterns = [
            r'\s*[-—–|•]\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # Any dash/punctuation + capitalized words
            r'\s*\([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\)$',        # Parentheses with capitalized words
            r'\s*\[[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\]$',        # Brackets with capitalized words
            # Very aggressive pattern for complex source attributions
            r'\s*-\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s*-\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*$',  # Multiple dash-separated capitalized phrases
        ]
        
        # Apply specific patterns first
        for pattern in source_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Then apply aggressive patterns
        for pattern in aggressive_patterns:
            text = re.sub(pattern, '', text)
        
        # Clean up any remaining trailing punctuation or whitespace
        text = re.sub(r'\s*[-—–|•]\s*$', '', text)
        text = text.strip()
        
        # Specific cleanup for common complex source patterns
        text = re.sub(r'\s*-\s*[A-Z][a-z]+\s+[A-Z][a-z]+\s*-\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s*,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*$', '', text)
        text = text.strip()
        
        # Common abbreviations and their spoken equivalents
        abbreviations = {
            r'\bCEO\b': 'Chief Executive Officer',
            r'\bCFO\b': 'Chief Financial Officer',
            r'\bCTO\b': 'Chief Technology Officer',
            r'\bCOO\b': 'Chief Operating Officer',
            r'\bVP\b': 'Vice President',
            r'\bAI\b': 'Artificial Intelligence',
            r'\bML\b': 'Machine Learning',
            r'\bAPI\b': 'A P I',
            r'\bGDP\b': 'Gross Domestic Product',
            r'\bFBI\b': 'F B I',
            r'\bCIA\b': 'C I A',
            r'\bNASA\b': 'N A S A',
            r'\bFDA\b': 'F D A',
            r'\bCDC\b': 'C D C',
            r'\bWHO\b': 'W H O',
            r'\bUN\b': 'United Nations',
            r'\bEU\b': 'European Union',
            r'\bUK\b': 'United Kingdom',
            r'\bUS\b': 'United States',
            r'\bUSA\b': 'United States of America',
            r'\bvs\b': 'versus',
            r'\bvs\.\b': 'versus',
            r'\b&': 'and',
            r'\b\+': 'plus',
            r'\b%': 'percent',
            r'\$(\d+)': r'\1 dollars',
            r'\$(\d+\.\d+)': r'\1 dollars',
            r'\b(\d+)%': r'\1 percent',
            r'\b(\d+)st\b': r'\1st',
            r'\b(\d+)nd\b': r'\1nd',
            r'\b(\d+)rd\b': r'\1rd',
            r'\b(\d+)th\b': r'\1th',
        }
        
        # Apply abbreviations
        for pattern, replacement in abbreviations.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Handle numbers and dates
        # Convert "2024" to "twenty twenty four" for years
        text = re.sub(r'\b(20\d{2})\b', lambda m: self._year_to_words(m.group(1)), text)
        
        # Handle common symbols
        text = text.replace('...', ' and so on')
        text = text.replace('--', ' to ')
        text = text.replace('–', ' to ')
        text = text.replace('—', ' to ')
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Capitalize first letter of sentences
        text = text[0].upper() + text[1:] if text else text
        
        return text
    
    def _year_to_words(self, year: str) -> str:
        """Convert year to spoken words"""
        if len(year) == 4:
            first_two = year[:2]
            last_two = year[2:]
            if first_two == '20':
                return f"twenty {self._number_to_words(int(last_two))}"
            elif first_two == '19':
                return f"nineteen {self._number_to_words(int(last_two))}"
        return year
    
    def _number_to_words(self, num: int) -> str:
        """Convert numbers 0-99 to words"""
        if num == 0:
            return "zero"
        elif num < 20:
            words = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
            return words[num]
        elif num < 100:
            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
            words = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
            if num % 10 == 0:
                return tens[num // 10]
            else:
                return f"{tens[num // 10]} {words[num % 10]}"
        return str(num)
    
    def get_news(self, category: str = "general", limit: int = 5) -> List[NewsItem]:
        """Get latest news articles"""
        if not self.api_key:
            # Mock news data when no API key is available
            return [
                NewsItem(
                    title="Artificial Intelligence breakthrough in medical diagnosis",
                    description="Researchers develop new AI system for early disease detection",
                    url="https://example.com/ai-medical",
                    source="Tech News",
                    published_at="2024-01-15T10:30:00Z"
                ),
                NewsItem(
                    title="Climate change summit results",
                    description="Global leaders agree on new environmental policies",
                    url="https://example.com/climate-summit",
                    source="World News",
                    published_at="2024-01-15T09:15:00Z"
                ),
                NewsItem(
                    title="Space exploration milestone",
                    description="New Mars rover discovers evidence of ancient water",
                    url="https://example.com/mars-discovery",
                    source="Science Daily",
                    published_at="2024-01-15T08:45:00Z"
                )
            ]
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={self.api_key}&pageSize={limit}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code != 200:
                return self._get_mock_news()
            
            articles = []
            for article in data.get('articles', []):
                # Make title TTS-friendly
                original_title = article.get('title', 'No title')
                tts_title = self._make_tts_friendly(original_title)
                
                # Debug: Print original vs processed title
                print(f"Original: '{original_title}'")
                print(f"Processed: '{tts_title}'")
                print("---")
                
                articles.append(NewsItem(
                    title=tts_title,
                    description=article.get('description', 'No description'),
                    url=article.get('url', '#'),
                    source=article.get('source', {}).get('name', 'Unknown'),
                    published_at=article.get('publishedAt', 'Unknown')
                ))
            
            return articles
        except Exception as e:
            print(f"News API error: {e}")
            return self._get_mock_news()
    
    def _get_mock_news(self) -> List[NewsItem]:
        """Get mock news data for testing"""
        return [
            NewsItem(
                title="Artificial Intelligence breakthrough in medical diagnosis",
                description="Researchers develop new AI system for early disease detection",
                url="https://example.com/ai-medical",
                source="Tech News",
                published_at="2024-01-15T10:30:00Z"
            ),
            NewsItem(
                title="Climate change summit results",
                description="Global leaders agree on new environmental policies",
                url="https://example.com/climate-summit",
                source="World News",
                published_at="2024-01-15T09:15:00Z"
            ),
            NewsItem(
                title="Space exploration milestone",
                description="New Mars rover discovers evidence of ancient water",
                url="https://example.com/mars-discovery",
                source="Science Daily",
                published_at="2024-01-15T08:45:00Z"
            )
        ]

# Global instance
news_service = NewsService() 