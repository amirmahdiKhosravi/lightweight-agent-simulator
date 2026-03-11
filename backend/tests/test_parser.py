import pytest
from parser import IntentParser


@pytest.fixture
def parser():
    return IntentParser()


def test_weather_intent_with_city(parser):
    out = parser.parse_intent("What's the weather in Toronto?")
    assert out["tool"] == "WeatherMockTool"
    assert out["arguments"]["city"] == "toronto"


def test_weather_intent_new_york(parser):
    out = parser.parse_intent("weather in new york")
    assert out["tool"] == "WeatherMockTool"
    assert out["arguments"]["city"] == "new york"


def test_weather_intent_default_city(parser):
    out = parser.parse_intent("weather")
    assert out["tool"] == "WeatherMockTool"
    assert out["arguments"]["city"] == "Toronto"


def test_calculator_intent(parser):
    out = parser.parse_intent("what is 2 + 3")
    assert out["tool"] == "CalculatorTool"
    assert out["arguments"]["expression"] == "what is 2 + 3"


def test_calculator_intent_subtraction(parser):
    out = parser.parse_intent("10 - 4")
    assert out["tool"] == "CalculatorTool"


def test_text_processor_uppercase_default(parser):
    out = parser.parse_intent("Hello World")
    assert out["tool"] == "TextProcessorTool"
    assert out["arguments"]["action"] == "uppercase"
    assert out["arguments"]["text"] == "Hello World"


def test_text_processor_lowercase(parser):
    out = parser.parse_intent("make this lower: FOO")
    assert out["tool"] == "TextProcessorTool"
    assert out["arguments"]["action"] == "lowercase"


def test_text_processor_word_count(parser):
    out = parser.parse_intent("count the words in this sentence")
    assert out["tool"] == "TextProcessorTool"
    assert out["arguments"]["action"] == "word_count"


def test_text_processor_words_keyword(parser):
    out = parser.parse_intent("how many words")
    assert out["tool"] == "TextProcessorTool"
    assert out["arguments"]["action"] == "word_count"
