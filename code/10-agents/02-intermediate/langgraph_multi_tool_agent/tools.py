from __future__ import annotations


def calculator(expression: str) -> str:
    allowed = set("0123456789.+-*/() ")
    if not set(expression) <= allowed:
        return "error: invalid characters"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"error: {exc}"


def search_mock(query: str) -> str:
    corpus = {
        "langgraph": "LangGraph is a library for building stateful, multi-actor LLM applications as graphs.",
        "react": "ReAct interleaves reasoning traces and tool actions to solve tasks.",
        "peft": "PEFT freezes base model weights and trains small adapter modules like LoRA.",
    }
    for key, value in corpus.items():
        if key in query.lower():
            return value
    return "no matching documents found"


def weather_mock(city: str) -> str:
    fake_weather = {"paris": "18C, cloudy", "delhi": "34C, sunny", "tokyo": "22C, rainy"}
    return fake_weather.get(city.strip().lower(), "unknown city, no forecast available")


TOOLS = {
    "calculator": calculator,
    "search": search_mock,
    "weather": weather_mock,
}
