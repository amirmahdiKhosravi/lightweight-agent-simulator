import pytest
from agent import Agent


@pytest.fixture
def agent():
    return Agent()


def test_agent_response_structure(agent):
    result = agent.execute_task("what is 2 + 3")
    assert "final_output" in result
    assert "execution_steps" in result
    assert "tools_used" in result
    assert "timestamp" in result
    assert isinstance(result["execution_steps"], list)
    assert isinstance(result["tools_used"], list)


def test_agent_happy_path_calculator(agent):
    result = agent.execute_task("5 + 3")
    assert result["final_output"] in ("8", "8.0")
    assert "CalculatorTool" in result["tools_used"]
    assert any("Received user task" in s for s in result["execution_steps"])
    assert any("Intent parsed" in s for s in result["execution_steps"])
    assert any("Executing" in s for s in result["execution_steps"])
    assert any("Returning final response" in s for s in result["execution_steps"])


def test_agent_happy_path_weather(agent):
    result = agent.execute_task("weather in London")
    assert "London" in result["final_output"]
    assert "WeatherMockTool" in result["tools_used"]


def test_agent_happy_path_text_processor(agent):
    # Parser sends full input as text with action uppercase
    result = agent.execute_task("hello")
    assert result["final_output"] == "HELLO"
    assert "TextProcessorTool" in result["tools_used"]


def test_agent_error_logged_in_trace(agent):
    # Parser returns CalculatorTool for input containing +; give invalid expression
    # so the calculator returns an error string (tool doesn't raise).
    result = agent.execute_task("foo + bar")
    assert "final_output" in result
    assert "execution_steps" in result
    assert any("Step X" in s or "Error" in s for s in result["execution_steps"])


def test_agent_tool_raises_caught(agent):
    # When a tool raises, agent should catch and log in trace without crashing
    original_execute = agent.tools["CalculatorTool"].execute
    agent.tools["CalculatorTool"].execute = lambda **kw: (_ for _ in ()).throw(ValueError("Tool failed"))
    result = agent.execute_task("2 + 3")
    assert "final_output" in result
    assert "error" in result["final_output"].lower() or "Tool failed" in result["final_output"]
    assert any("Step X" in s or "error" in s.lower() or "Tool failed" in s for s in result["execution_steps"])
    agent.tools["CalculatorTool"].execute = original_execute
