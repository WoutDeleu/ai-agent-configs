# LangGraph

Config templates for LangGraph stateful agent graphs.

## Key concepts

- **StateGraph**: a graph where each node reads and writes shared state
- **Node**: a function that takes state and returns a state update
- **Edge**: a connection between nodes; can be conditional
- **Checkpointer**: persists graph state between invocations (e.g. SQLite, Postgres)

## Files

- `graph.example.py` — minimal ReAct-style graph skeleton
