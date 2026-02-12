# AWS Strands

![Intro Lecture AWS Strands Thumb](Intro%20Lecture%20AWS%20Strands%20Thumb.png)

Examples and utilities for building **agentic AI** applications with the [Strands](https://github.com/aws/strands) framework and **Amazon Bedrock** models (e.g. Claude, Nova).

## Overview

This repo contains:

- **Basic Strands usage** – simple agents with Bedrock models
- **Custom tools** – calculator, word count, and HTTP request tools
- **Structured output** – Pydantic schemas for typed LLM responses
- **API integration** – FastAPI sample API and agents that call it via `http_request`
- **Data utilities** – pushing JSON data to DynamoDB

## Prerequisites

- **Python 3.x**
- **AWS credentials** configured (e.g. `~/.aws/credentials` or environment variables) with access to **Amazon Bedrock**
- **Bedrock model access** in your AWS account (e.g. Claude, Nova)

## Setup

```bash
# Clone and enter the repo
cd aws_strands

# Recommended: use a virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies (Strands, Bedrock, FastAPI, etc.)
pip install strands strands-tools pydantic fastapi uvicorn boto3
```

## Project Structure

| File | Description |
|------|-------------|
| `basic-use.py` | Minimal Strands agent with a Bedrock model ID |
| `aws_strands_bedrockmodels.py` | Agent using `BedrockModel` with streaming and temperature |
| `custom_tool_agent.py` | Agent with a custom `@tool` (e.g. word count) |
| `calculator_tool.py` | Agent with a calculator tool |
| `aws_http_request_tool.py` | Agent using `http_request` to call APIs |
| `http-tool-use.py` | Dog-breed helper agent with system prompt and HTTP tool |
| `aws_strands_structured_output.py` | Structured output with Pydantic (`ProductAnalysis`) |
| `system-prompt-use.py` | Agent with a custom system prompt |
| `custom_api_tool_agent.py` | Agent wired to a custom API |
| `main_api.py` | FastAPI app serving currency rates from `rates.json` |
| `push_data_from_json_to_dynamodb.py` | Load JSON data and push to DynamoDB |
| `selected_llm.py` | LLM selection / configuration example |
| `rates.json` | Sample data for the currency-rate API |
| `tickets_dataset/` | Sample ticket JSON files for demos |

## Quick Start

**1. Simple agent (no tools):**

```bash
python basic-use.py
```

**2. Agent with BedrockModel and streaming:**

```bash
python aws_strands_bedrockmodels.py
```

**3. Agent with HTTP tool (calls your API):**

Start the sample API, then run the agent:

```bash
# Terminal 1: start the rates API
uvicorn main_api:app --reload --port 5000

# Terminal 2: run the agent (update system prompt if your API URL/port differs)
python aws_http_request_tool.py
```

**4. Structured output:**

```bash
python aws_strands_structured_output.py
```

## Configuration

- **Model ID**: Scripts use Bedrock model IDs such as `us.anthropic.claude-3-5-sonnet-20241022-v2:0` or `us.amazon.nova-pro-v1:0`. Change these in the scripts to match the models enabled in your account.
- **Region**: Set `region_name` in `BedrockModel(...)` if you use a region other than `us-east-1`.
- **API base URL**: In `aws_http_request_tool.py`, the system prompt references `http://localhost:5000/`; adjust if your API runs elsewhere.

## License

See repository license information.
