# Agent hooks (AWS Strands)


![Intro Lecture AWS Strands Thumb](AWS%20Strands%20Agents%20Hooks%20and%20Callbacks%20label.png)

Small Python examples that show how to observe an [AWS Strands](https://github.com/strands-agents/sdk-python) `Agent` with lifecycle hooks while using **Amazon Bedrock** (`BedrockModel`, Nova).

## Contents

| File | What it demonstrates |
|------|----------------------|
| `simple_agent_hooksregistry.py` | Hooks registered through a **`HookRegistry`**-style object: a class with `register_hooks(registry, **kwargs)` and `registry.add_callback(...)` for many event types. |
| `simple_agent_selected_hooks.py` | The same hook *logic* attached **after** the agent is built with **`agent.hooks.add_callback(...)`** and plain functions (subset of events). |

Both scripts print hook traces to the console (messages, tool calls, model calls, invocation boundaries).

## Prerequisites

- Python 3.10+ (recommended)
- Installed packages used by the scripts, for example:
  - `strands` (Strands SDK)
  - `strands-tools` (optional tools such as `calculator`, `current_time`)
  - AWS SDK / credentials configured so **`BedrockModel`** can call Bedrock (model access in your account/region)

Exact install steps depend on how you manage the parent `AWS_Strands` project; use the same environment you use for other Strands samples there.

## Configuration

Both examples use:

- **Model:** `us.amazon.nova-pro-v1:0`
- **Streaming:** enabled on the Bedrock model

Adjust `model_id`, region, or credentials in line with your AWS setup before running.

## Run

From this directory (with your virtual environment activated if you use one):

```bash
python simple_agent_hooksregistry.py
```

```bash
python simple_agent_selected_hooks.py
```

Each file runs a short demo query at the end of the script.

## Hook events used

**Registry example** (`simple_agent_hooksregistry.py`): `AgentInitialized`, `BeforeInvocation`, `AfterInvocation`, `MessageAdded`, `BeforeToolCall`, `AfterToolCall`, `BeforeModelCall`, `AfterModelCall`.

**Selected callbacks** (`simple_agent_selected_hooks.py`): `MessageAdded`, `BeforeToolCall`, `AfterToolCall`, `BeforeModelCall`, `AfterModelCall`.

Use the registry pattern when you want a reusable “plugin” class; use `agent.hooks.add_callback` when you prefer minimal wiring on an existing agent instance.
