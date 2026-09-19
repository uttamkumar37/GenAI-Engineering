# requires ANTHROPIC_API_KEY for the real client; FakeToolCallingLLM needs nothing
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get the current mock weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
    {
        "name": "search",
        "description": "Search a mock knowledge base for a query.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
]

_MOCK_WEATHER = {"paris": "18C, cloudy", "tokyo": "24C, sunny", "delhi": "34C, hazy"}
_MOCK_SEARCH = {
    "anthropic founding": "Anthropic was founded in 2021 by former OpenAI researchers.",
}


def run_tool(name: str, tool_input: dict[str, Any]) -> str:
    if name == "calculator":
        try:
            return str(eval(tool_input["expression"], {"__builtins__": {}}, {}))
        except Exception as exc:
            return f"error: {exc}"
    if name == "get_weather":
        return _MOCK_WEATHER.get(tool_input["city"].lower(), "unknown city")
    if name == "search":
        query = tool_input["query"].lower()
        for key, value in _MOCK_SEARCH.items():
            if key in query:
                return value
        return "no results found"
    return "unknown tool"


@dataclass
class ToolCall:
    id: str
    name: str
    input: dict[str, Any]


@dataclass
class AssistantTurn:
    text: str | None
    tool_calls: list[ToolCall]


class ToolCallingLLM(ABC):
    @abstractmethod
    def step(self, messages: list[dict]) -> AssistantTurn: ...


class AnthropicToolCallingLLM(ToolCallingLLM):
    def __init__(self, model: str = "claude-opus-5") -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def step(self, messages: list[dict]) -> AssistantTurn:
        response = self.client.messages.create(
            model=self.model, max_tokens=512, tools=TOOLS, messages=messages
        )
        text = next((b.text for b in response.content if b.type == "text"), None)
        calls = [
            ToolCall(id=b.id, name=b.name, input=b.input)
            for b in response.content
            if b.type == "tool_use"
        ]
        messages.append({"role": "assistant", "content": response.content})
        return AssistantTurn(text=text, tool_calls=calls)


class FakeToolCallingLLM(ToolCallingLLM):
    # deterministic keyword-routing stand-in, no network required
    def step(self, messages: list[dict]) -> AssistantTurn:
        last = messages[-1]
        if last["role"] == "user" and isinstance(last["content"], str):
            query = last["content"].lower()
            if any(op in query for op in ["+", "-", "*", "/", "calculate"]):
                expr = "".join(ch for ch in query if ch.isdigit() or ch in "+-*/(). ")
                call = ToolCall(id="call_1", name="calculator", input={"expression": expr.strip()})
            elif "weather" in query:
                city = next((c for c in _MOCK_WEATHER if c in query), "paris")
                call = ToolCall(id="call_1", name="get_weather", input={"city": city})
            else:
                call = ToolCall(id="call_1", name="search", input={"query": query})
            messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "tool_use", "id": call.id, "name": call.name, "input": call.input}],
                }
            )
            return AssistantTurn(text=None, tool_calls=[call])
        # second step: synthesize a final answer from the tool result
        tool_result_text = last["content"][0]["content"]
        final = f"Based on the tool result: {tool_result_text}"
        messages.append({"role": "assistant", "content": final})
        return AssistantTurn(text=final, tool_calls=[])


def run_agentic_loop(llm: ToolCallingLLM, user_message: str) -> str:
    messages: list[dict] = [{"role": "user", "content": user_message}]
    turn = llm.step(messages)
    while turn.tool_calls:
        results = [
            {"type": "tool_result", "tool_use_id": call.id, "content": run_tool(call.name, call.input)}
            for call in turn.tool_calls
        ]
        messages.append({"role": "user", "content": results})
        turn = llm.step(messages)
    return turn.text or ""


if __name__ == "__main__":
    llm: ToolCallingLLM = (
        AnthropicToolCallingLLM() if os.environ.get("ANTHROPIC_API_KEY") else FakeToolCallingLLM()
    )
    for question in ["What's 12 * 7?", "What's the weather in Tokyo?", "Tell me about Anthropic founding"]:
        print(f"Q: {question}")
        print(f"A: {run_agentic_loop(llm, question)}\n")
