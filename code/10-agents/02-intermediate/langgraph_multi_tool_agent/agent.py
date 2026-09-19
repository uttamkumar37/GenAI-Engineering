from __future__ import annotations

# written against langgraph's StateGraph API (graph.add_node/add_edge/compile) as of the
# 0.2.x stable line; verify against `pip show langgraph` before relying on this in production
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

from fake_llm import FakeLLM
from tools import TOOLS


class AgentState(TypedDict):
    task: str
    plan: list[str]
    remaining_subtasks: list[str]
    observations: Annotated[list[str], operator.add]
    final_answer: str


llm = FakeLLM()


def plan_node(state: AgentState) -> dict:
    subtasks = llm.plan(state["task"])
    return {"plan": subtasks, "remaining_subtasks": subtasks}


def execute_node(state: AgentState) -> dict:
    remaining = list(state["remaining_subtasks"])
    subtask = remaining.pop(0)
    tool_name, tool_arg = llm.choose_tool(subtask, state["task"])

    tool_fn = TOOLS.get(tool_name)
    observation = tool_fn(tool_arg) if tool_fn else f"skipped '{subtask}', no matching tool"

    return {
        "remaining_subtasks": remaining,
        "observations": [f"[{subtask}] {observation}"],
    }


def should_continue(state: AgentState) -> str:
    return "execute" if state["remaining_subtasks"] else "synthesize"


def synthesize_node(state: AgentState) -> dict:
    return {"final_answer": llm.synthesize(state["task"], state["observations"])}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("plan", plan_node)
    graph.add_node("execute", execute_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "execute")
    graph.add_conditional_edges(
        "execute", should_continue, {"execute": "execute", "synthesize": "synthesize"}
    )
    graph.add_edge("synthesize", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke(
        {
            "task": "What is the weather in Tokyo and what is 4 * 9?",
            "plan": [],
            "remaining_subtasks": [],
            "observations": [],
            "final_answer": "",
        }
    )
    print("Plan:", result["plan"])
    print("Observations:", result["observations"])
    print("Final answer:", result["final_answer"])
