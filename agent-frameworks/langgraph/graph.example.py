"""Minimal LangGraph ReAct agent skeleton."""
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


def call_llm(state: State) -> dict:
    # Replace with your LLM call
    raise NotImplementedError


def should_continue(state: State) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return END


graph = (
    StateGraph(State)
    .add_node("llm", call_llm)
    .add_conditional_edges("llm", should_continue)
    .set_entry_point("llm")
    .compile()
)
