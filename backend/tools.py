"""
Tool implementations for the agent simulator.

Every tool inherits from :class:`BaseTool` and exposes an ``execute(**kwargs)``
method that returns a human-readable string result.
"""

import re
from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Abstract base class that all tools must inherit from."""

    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool's core logic and return a string result."""
        pass


class TextProcessorTool(BaseTool):
    """Applies simple text transformations: upper-case, lower-case, or word count."""

    name = "TextProcessorTool"
    description = "Modifies text. Actions: 'uppercase', 'lowercase', 'word_count'."

    def execute(self, text: str = "", action: str = "uppercase", **kwargs) -> str:
        """
        Transform *text* according to the requested *action*.

        Args:
            text:   The input string to process.
            action: One of ``"uppercase"``, ``"lowercase"``, or ``"word_count"``.

        Returns:
            The transformed text, or an error message on invalid input.
        """
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
    """Evaluates a single binary arithmetic expression (e.g. ``3 + 5``)."""

    name = "CalculatorTool"
    description = "Performs basic arithmetic (e.g., 3 + 5)."

    # Matches "<number> <op> <number>" — supports optional decimals and
    # negative signs.  Intentionally avoids ``eval()`` for safety.
    _EXPR_RE = re.compile(
        r'(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)'
    )

    def execute(self, expression: str = "", **kwargs) -> str:
        """
        Parse and evaluate a simple math *expression*.

        Args:
            expression: A string like ``"5 + 3"`` or ``"10 / 2.5"``.

        Returns:
            The numeric result as a string, or an error message.
        """
        if not expression:
            return "Error: No expression provided."

        match = self._EXPR_RE.search(expression)
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
    """Returns hard-coded weather data so the simulator needs no external API."""

    name = "WeatherMockTool"
    description = "Returns mock weather data for a given city."

    _MOCK_DATA = {
        "toronto": "15°C and partly cloudy.",
        "new york": "18°C and sunny.",
        "london": "10°C and rainy.",
        "mississauga": "14°C and breezy.",
    }

    def execute(self, city: str = "Unknown", **kwargs) -> str:
        """
        Look up mock weather for *city*.

        Args:
            city: City name (case-insensitive).

        Returns:
            A sentence describing the weather.  Unknown cities get a
            generic fallback (``"20°C and clear."``).
        """
        weather = self._MOCK_DATA.get(city.lower().strip(), "20°C and clear.")
        return f"The weather in {city.title()} is {weather}"
