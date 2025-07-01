"""
Calculator service for Prism AI Voice Assistant
Provides mathematical calculation capabilities
"""

import re
from typing import Union

class CalculatorService:
    """Service for mathematical calculations"""
    
    def calculate(self, expression: str) -> str:
        """Simple calculator function"""
        try:
            # Remove common words and keep only mathematical expression
            expression = re.sub(r'\b(what is|calculate|compute|solve|what\'s)\b', '', expression, flags=re.IGNORECASE)
            expression = expression.strip()
            
            # Remove question marks and other punctuation
            expression = re.sub(r'[?.,!]', '', expression)
            
            # Replace words with symbols
            expression = expression.replace('plus', '+')
            expression = expression.replace('minus', '-')
            expression = expression.replace('times', '*')
            expression = expression.replace('multiplied by', '*')
            expression = expression.replace('divided by', '/')
            expression = expression.replace('divided', '/')
            
            # Clean up the expression
            expression = re.sub(r'\s+', '', expression)
            
            # Validate expression contains only safe characters
            if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
                return "I can only perform basic mathematical operations (+, -, *, /)"
            
            # Evaluate the expression
            result = eval(expression)
            
            # Convert result to plain text for better TTS pronunciation
            if isinstance(result, (int, float)):
                if result == int(result):
                    # Convert integer to words
                    return self._number_to_words(int(result))
                else:
                    # Convert decimal to words
                    return self._decimal_to_words(result)
            else:
                return str(result)
                
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    def _number_to_words(self, num: int) -> str:
        """Convert integer to words for TTS pronunciation"""
        if num == 0:
            return "zero"
        
        # Handle negative numbers
        if num < 0:
            return f"negative {self._number_to_words(abs(num))}"
        
        # Handle large numbers
        if num >= 1000000:
            millions = num // 1000000
            remainder = num % 1000000
            if remainder == 0:
                return f"{self._number_to_words(millions)} million"
            else:
                return f"{self._number_to_words(millions)} million {self._number_to_words(remainder)}"
        
        if num >= 1000:
            thousands = num // 1000
            remainder = num % 1000
            if remainder == 0:
                return f"{self._number_to_words(thousands)} thousand"
            else:
                return f"{self._number_to_words(thousands)} thousand {self._number_to_words(remainder)}"
        
        if num >= 100:
            hundreds = num // 100
            remainder = num % 100
            if remainder == 0:
                return f"{self._number_to_words(hundreds)} hundred"
            else:
                return f"{self._number_to_words(hundreds)} hundred {self._number_to_words(remainder)}"
        
        # Handle numbers 0-99
        if num <= 20:
            return self._ones_and_teens(num)
        else:
            tens = (num // 10) * 10
            ones = num % 10
            if ones == 0:
                return self._tens(tens)
            else:
                return f"{self._tens(tens)} {self._ones_and_teens(ones)}"
    
    def _ones_and_teens(self, num: int) -> str:
        """Convert numbers 0-20 to words"""
        words = {
            0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
            11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
            16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"
        }
        return words.get(num, str(num))
    
    def _tens(self, num: int) -> str:
        """Convert tens (20, 30, 40, etc.) to words"""
        words = {
            20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
            60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"
        }
        return words.get(num, str(num))
    
    def _decimal_to_words(self, num: float) -> str:
        """Convert decimal number to words for TTS pronunciation"""
        # Split into integer and decimal parts
        integer_part = int(num)
        decimal_part = round(num - integer_part, 2)
        
        # Convert integer part
        integer_words = self._number_to_words(integer_part)
        
        # Handle decimal part
        if decimal_part == 0:
            return integer_words
        
        # Convert decimal to words
        decimal_str = f"{decimal_part:.2f}".split('.')[1]
        decimal_words = self._decimal_part_to_words(decimal_str)
        
        return f"{integer_words} point {decimal_words}"
    
    def _decimal_part_to_words(self, decimal_str: str) -> str:
        """Convert decimal part to words"""
        words = []
        for digit in decimal_str:
            if digit == '0':
                words.append("zero")
            else:
                words.append(self._ones_and_teens(int(digit)))
        return " ".join(words)

# Global instance
calculator_service = CalculatorService() 