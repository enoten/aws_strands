from strands import Agent
from strands.hooks import AfterModelCallEvent, AfterToolCallEvent, BeforeModelCallEvent, BeforeToolCallEvent, MessageAddedEvent
from strands.models import BedrockModel

from strands import tool
from strands_tools import calculator

# Define a custom tool
@tool
def get_weather(location: str) -> str:
    """
    Get the current weather for a location.

    Args:
        location: City name or location

    Returns:
        Weather information
    """
    # In a real application, call a weather API
    return f"The weather in {location} is sunny and 72°F"


def message_to_text(message: dict | None) -> str:
    if not message:
        return ""

    parts = []
    for content in message.get("content", []):
        if "text" in content:
            parts.append(content["text"])
        elif "toolUse" in content:
            parts.append(f"[tool use: {content['toolUse'].get('name', 'unknown')}]")
        elif "toolResult" in content:
            parts.append("[tool result]")
        else:
            parts.append(str(content))

    return "\n".join(parts)



# Bedrock
print("\n\n ===== Amazon Nova =====")
bedrock_model = BedrockModel(
model_id="us.amazon.nova-pro-v1:0",
temperature=0.3,
streaming=True, # Enable/disable streaming
)

agent = Agent(
    model=bedrock_model,
    tools=[get_weather,calculator],
    system_prompt="You are a helpful assistant with access to tools.",
)

def on_message_added(event: MessageAddedEvent) -> None:
    role = event.message.get("role", "unknown")
    print(f"\n >>> Message added ({role}): {message_to_text(event.message)}")

def on_before_tool_call(event: BeforeToolCallEvent) -> None:
    print(f"\n >>> Before tool call: {event.tool_use['name']}")

def on_after_tool_call(event: AfterToolCallEvent) -> None:
    if event.exception:
        print(f"\n >>> After tool call: {event.tool_use['name']} failed: {event.exception}")
    else:
        print(f"\n >>> After tool call: {event.tool_use['name']} result={event.result}")

def on_before_model_call( event: BeforeModelCallEvent) -> None:
    print(f"\n >>> Before model call: {len(event.agent.messages)} message(s)")

def on_after_model_call( event: AfterModelCallEvent) -> None:
    if event.exception:
        print(f"\n >>> After model call failed: {event.exception}")
        return

    if event.stop_response:
        print(f"\n >>> After model call: {message_to_text(event.stop_response.message)}")
    else:
        print("\n >>> After model call: no response")

agent.hooks.add_callback(MessageAddedEvent, on_message_added)
agent.hooks.add_callback(BeforeToolCallEvent, on_before_tool_call)
agent.hooks.add_callback(AfterToolCallEvent, on_after_tool_call)
agent.hooks.add_callback(BeforeModelCallEvent, on_before_model_call)
agent.hooks.add_callback(AfterModelCallEvent, on_after_model_call)

query ="""
What is 25 times 7?
"""

print(agent(query))



