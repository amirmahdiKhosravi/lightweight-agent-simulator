"""
Rule-based intent parser.

Replaces an LLM call with deterministic keyword/regex matching so the
simulator stays lightweight and needs no external API keys.
"""

import re


class IntentParser:
    """
    Classifies free-text user input into a structured ``{tool, arguments}``
    payload that the :class:`Agent` can dispatch to the correct tool.

    Priority order: Weather > Calculator > TextProcessor (fallback).
    """

    def parse_intent(self, user_input: str) -> dict:
        """
        Parse *user_input* and return the tool name + arguments to invoke.

        Args:
            user_input: Raw text entered by the user.

        Returns:
            dict with ``"tool"`` (str) and ``"arguments"`` (dict) keys.
        """
        text_lower = user_input.lower().strip()

        # --- Weather intent -------------------------------------------------
        if "weather" in text_lower:
            # Try to grab the city after "in <city>"; fall back to Toronto
            match = re.search(r'in\s+([a-zA-Z\s]+)', text_lower)
            city = match.group(1).strip() if match else "Toronto"
            return {
                "tool": "WeatherMockTool",
                "arguments": {"city": city},
            }

        # --- Calculator intent ----------------------------------------------
        # Any arithmetic operator triggers the calculator
        if re.search(r'[\+\-\*\/]', text_lower):
            return {
                "tool": "CalculatorTool",
                "arguments": {"expression": text_lower},
            }

        # --- Text processor (fallback) --------------------------------------
        action = "uppercase"
        if "count" in text_lower or "words" in text_lower:
            action = "word_count"
        elif "lower" in text_lower:
            action = "lowercase"

        return {
            "tool": "TextProcessorTool",
            "arguments": {"text": user_input, "action": action},
        }
