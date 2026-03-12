"""Unit tests for individual tool implementations."""

import pytest
from tools import CalculatorTool, WeatherMockTool, TextProcessorTool


# --- CalculatorTool ---

@pytest.fixture
def calc():
    return CalculatorTool()


def test_calculator_add(calc):
    assert calc.execute(expression="5 + 3") in ("8", "8.0")


def test_calculator_subtract(calc):
    assert calc.execute(expression="10 - 4") in ("6", "6.0")


def test_calculator_multiply(calc):
    assert calc.execute(expression="6 * 7") in ("42", "42.0")


def test_calculator_divide(calc):
    assert calc.execute(expression="15 / 3") == "5.0"


def test_calculator_division_by_zero(calc):
    assert "Division by zero" in calc.execute(expression="1 / 0")


def test_calculator_unparseable(calc):
    out = calc.execute(expression="not a math expression")
    assert "Error" in out and "parse" in out.lower()


def test_calculator_empty_expression(calc):
    out = calc.execute(expression="")
    assert "Error" in out


# --- WeatherMockTool ---

@pytest.fixture
def weather():
    return WeatherMockTool()


def test_weather_known_city_toronto(weather):
    out = weather.execute(city="Toronto")
    assert "Toronto" in out
    assert "15" in out or "partly cloudy" in out.lower()


def test_weather_known_city_london(weather):
    out = weather.execute(city="london")
    assert "London" in out
    assert "10" in out or "rainy" in out.lower()


def test_weather_unknown_city(weather):
    out = weather.execute(city="UnknownCity")
    # .title() yields "Unknowncity"; fallback weather is returned
    assert "weather" in out.lower() and ("20" in out or "clear" in out.lower())


# --- TextProcessorTool ---

@pytest.fixture
def text_proc():
    return TextProcessorTool()


def test_text_processor_uppercase(text_proc):
    assert text_proc.execute(text="hello", action="uppercase") == "HELLO"


def test_text_processor_lowercase(text_proc):
    assert text_proc.execute(text="WORLD", action="lowercase") == "world"


def test_text_processor_word_count(text_proc):
    out = text_proc.execute(text="one two three", action="word_count")
    assert "3" in out


def test_text_processor_empty_text(text_proc):
    out = text_proc.execute(text="", action="uppercase")
    assert "Error" in out


def test_text_processor_unknown_action(text_proc):
    out = text_proc.execute(text="hi", action="invalid")
    assert "Error" in out
    assert "invalid" in out.lower()
