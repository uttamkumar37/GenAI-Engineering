# requires ANTHROPIC_API_KEY for the real client; FakeChainLLM needs nothing
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")

TOOLS = [
    {
        "name": "lookup_hq_city",
        "description": "Look up the city where a company's headquarters is located.",
        "input_schema": {
            "type": "object",
            "properties": {"company": {"type": "string"}},
            "required": ["company"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get current mock weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
]

_HQ_CITY = {"anthropic": "San Francisco", "openai": "San Francisco", "qdrant": "Berlin"}
_WEATHER = {"san francisco": "16C, foggy", "berlin": "12C, overcast"}


def run_tool(name: str, tool_input: dict[str, Any]) -> str:
    if name == "lookup_hq_city":
        return _HQ_CITY.get(tool_input["company"].lower(), "unknown")
    if name == "get_weather":
        return _WEATHER.get(tool_input["city"].lower(), "unknown")
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


class ChainLLM(ABC):
    @abstractmethod
    def step(self, messages: list[dict]) -> AssistantTurn: ...


class AnthropicChainLLM(ChainLLM):
    def __init__(self, model: str = MODEL) -> None:
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


class FakeChainLLM(ChainLLM):
    # deterministic 2-hop plan: lookup_hq_city -> get_weather -> final answer
    def __init__(self) -> None:
        self._step_index = 0

    def step(self, messages: list[dict]) -> AssistantTurn:
        if self._step_index == 0:
            user_text = messages[0]["content"].lower()
            company = next((c for c in _HQ_CITY if c in user_text), "anthropic")
            call = ToolCall(id="call_1", name="lookup_hq_city", input={"company": company})
            self._step_index += 1
            messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "tool_use", "id": call.id, "name": call.name, "input": call.input}],
                }
            )
            return AssistantTurn(text=None, tool_calls=[call])
        if self._step_index == 1:
            city = messages[-1]["content"][0]["content"]
            call = ToolCall(id="call_2", name="get_weather", input={"city": city})
            self._step_index += 1
            messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "tool_use", "id": call.id, "name": call.name, "input": call.input}],
                }
            )
            return AssistantTurn(text=None, tool_calls=[call])
        weather = messages[-1]["content"][0]["content"]
        final = f"The weather at the company's HQ is currently {weather}."
        messages.append({"role": "assistant", "content": final})
        return AssistantTurn(text=final, tool_calls=[])


def run_chain(llm: ChainLLM, user_message: str) -> str:
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
    llm: ChainLLM = AnthropicChainLLM() if os.environ.get("ANTHROPIC_API_KEY") else FakeChainLLM()
    print(run_chain(llm, "What's the weather like where Anthropic is headquartered?"))
