# LangChain

Config templates for LangChain and LCEL (LangChain Expression Language) agents.

## Files

- `agent.example.yaml` — base agent configuration

## Key concepts

- **Chain**: a sequence of LLM calls and tool invocations
- **Agent**: a chain that decides at runtime which tools to call
- **Tool**: a function exposed to the agent (search, code execution, etc.)
