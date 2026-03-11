import re

class IntentParser:
    """
    Simulates an LLM parsing user input and returning a structured payload.
    Uses deterministic rule-based matching to satisfy the 'lightweight' requirement
    without needing external API calls or heavy local models.
    """
    
    def parse_intent(self, user_input: str) -> dict:
        text_lower = user_input.lower().strip()
        
        # 1. Check for Weather Intent
        if "weather" in text_lower:
            # Extract the city name, usually following the word "in"
            match = re.search(r'in\s+([a-zA-Z\s]+)', text_lower)
            city = match.group(1).strip() if match else "Toronto" # Safe default
            return {
                "tool": "WeatherMockTool",
                "arguments": {"city": city}
            }
            
        # 2. Check for Calculator Intent
        # Look for basic math operators (+, -, *, /)
        if re.search(r'[\+\-\*\/]', text_lower):
            return {
                "tool": "CalculatorTool",
                "arguments": {"expression": text_lower}
            }
            
        # 3. Default to Text Processor Intent
        # Determine the action based on keywords
        action = "uppercase"
        if "count" in text_lower or "words" in text_lower:
            action = "word_count"
        elif "lower" in text_lower:
            action = "lowercase"
            
        return {
            "tool": "TextProcessorTool",
            "arguments": {"text": user_input, "action": action}
        }
