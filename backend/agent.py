"""
Agent orchestrator.

Implements the core parse → resolve → execute pipeline and records
every intermediate step into an execution trace for the frontend.
"""

from datetime import datetime
from tools import CalculatorTool, WeatherMockTool, TextProcessorTool
from parser import IntentParser


class Agent:
    """
    The main controller that orchestrates the Parser and the Tools.
    Builds the step-by-step execution trace required by the frontend.
    """

    def __init__(self):
        self.tools = {
            "CalculatorTool": CalculatorTool(),
            "WeatherMockTool": WeatherMockTool(),
            "TextProcessorTool": TextProcessorTool(),
        }
        self.parser = IntentParser()

    def execute_task(self, user_input: str) -> dict:
        """
        Run the full agent pipeline for a single user query.

        Args:
            user_input: Free-text task submitted by the user.

        Returns:
            dict matching the ``AgentResponse`` schema with keys
            *final_output*, *execution_steps*, *tools_used*, and *timestamp*.
        """
        execution_steps = []
        tools_used = []

        execution_steps.append(f"Step 1: Received user task: '{user_input}'")

        try:
            parsed_plan = self.parser.parse_intent(user_input)
            tool_name = parsed_plan["tool"]
            tool_args = parsed_plan["arguments"]

            execution_steps.append(
                f"Step 2: Intent parsed. Selected tool: {tool_name} with args: {tool_args}"
            )
            tools_used.append(tool_name)

            selected_tool = self.tools.get(tool_name)
            if not selected_tool:
                raise ValueError(f"Tool '{tool_name}' not found in registry.")

            execution_steps.append(f"Step 3: Executing {tool_name}...")
            result = selected_tool.execute(**tool_args)

            execution_steps.append(f"Step 4: Tool execution successful. Result: {result}")
            final_output = result

        except Exception as e:
            error_msg = f"Agent encountered an error: {str(e)}"
            execution_steps.append(f"Step X: {error_msg}")
            final_output = error_msg

        execution_steps.append("Step 5: Returning final response to user.")

        return {
            "final_output": final_output,
            "execution_steps": execution_steps,
            "tools_used": tools_used,
            "timestamp": datetime.utcnow(),
        }
