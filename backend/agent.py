from datetime import datetime
from tools import CalculatorTool, WeatherMockTool, TextProcessorTool
from parser import IntentParser

class Agent:
    """
    The main controller that orchestrates the Parser and the Tools.
    Builds the step-by-step execution trace required by the frontend.
    """
    def __init__(self):
        # Initialize tools into a dictionary for O(1) lookup
        self.tools = {
            "CalculatorTool": CalculatorTool(),
            "WeatherMockTool": WeatherMockTool(),
            "TextProcessorTool": TextProcessorTool()
        }
        self.parser = IntentParser()

    def execute_task(self, user_input: str) -> dict:
        execution_steps = []
        tools_used = []
        
        execution_steps.append(f"Step 1: Received user task: '{user_input}'")
        
        try:
            # Step 1: Parse the intent
            parsed_plan = self.parser.parse_intent(user_input)
            tool_name = parsed_plan["tool"]
            tool_args = parsed_plan["arguments"]
            
            execution_steps.append(f"Step 2: Intent parsed. Selected tool: {tool_name} with args: {tool_args}")
            tools_used.append(tool_name)
            
            # Step 2: Fetch the tool
            selected_tool = self.tools.get(tool_name)
            if not selected_tool:
                raise ValueError(f"Tool '{tool_name}' not found in registry.")
            
            # Step 3: Execute the tool
            execution_steps.append(f"Step 3: Executing {tool_name}...")
            result = selected_tool.execute(**tool_args)
            
            execution_steps.append(f"Step 4: Tool execution successful. Result: {result}")
            final_output = result
            
        except Exception as e:
            # Graceful error handling
            error_msg = f"Agent encountered an error: {str(e)}"
            execution_steps.append(f"Step X: {error_msg}")
            final_output = error_msg
        
        execution_steps.append("Step 5: Returning final response to user.")
        
        # We return a dictionary that perfectly matches our Pydantic AgentResponse schema
        return {
            "final_output": final_output,
            "execution_steps": execution_steps,
            "tools_used": tools_used,
            "timestamp": datetime.utcnow()
        }
