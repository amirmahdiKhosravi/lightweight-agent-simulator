import re
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Abstract base class that all tools must inherit from."""
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Executes the tool's core logic."""
        pass

class TextProcessorTool(BaseTool):
    name = "TextProcessorTool"
    description = "Modifies text. Actions: 'uppercase', 'lowercase', 'word_count'."

    def execute(self, text: str = "", action: str = "uppercase", **kwargs) -> str:
        if not text:
            return "Error: No text provided."
        
        action = action.lower()
        if action == "uppercase":
            return text.upper()
        elif action == "lowercase":
            return text.lower()
        elif action == "word_count":
            return f"Word count: {len(text.split())}"
        else:
            return f"Error: Unknown action '{action}'."

class CalculatorTool(BaseTool):
    name = "CalculatorTool"
    description = "Performs basic arithmetic (e.g., 3 + 5)."

    def execute(self, expression: str = "", **kwargs) -> str:
        if not expression:
            return "Error: No expression provided."
            
        # Safely parse basic math without using the dangerous eval() function
        match = re.search(r'(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)', expression)
        if not match:
            return "Error: Could not parse a valid simple math expression (e.g., 5 + 3)."

        num1, operator, num2 = float(match.group(1)), match.group(2), float(match.group(3))
        
        try:
            if operator == '+': return str(num1 + num2)
            if operator == '-': return str(num1 - num2)
            if operator == '*': return str(num1 * num2)
            if operator == '/': return str(num1 / num2)
        except ZeroDivisionError:
            return "Error: Division by zero."

class WeatherMockTool(BaseTool):
    name = "WeatherMockTool"
    description = "Returns mock weather data for a given city."

    def execute(self, city: str = "Unknown", **kwargs) -> str:
        # Mocking data to avoid external API calls per requirements
        city_lower = city.lower().strip()
        mock_data = {
            "toronto": "15°C and partly cloudy.",
            "new york": "18°C and sunny.",
            "london": "10°C and rainy.",
            "mississauga": "14°C and breezy."
        }
        
        # Default fallback if city isn't in our mock dictionary
        weather = mock_data.get(city_lower, "20°C and clear.")
        return f"The weather in {city.title()} is {weather}"
