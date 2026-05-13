from strands import Agent
from strands.hooks.events import (
    AfterInvocationEvent,
    AfterModelCallEvent,
    AfterToolCallEvent,
    AgentInitializedEvent,
    BeforeInvocationEvent,
    BeforeModelCallEvent,
    BeforeToolCallEvent,
    MessageAddedEvent,
)
from strands.hooks.registry import HookRegistry
from strands.models import BedrockModel

from strands import tool
from strands_tools import calculator, current_time


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


class AllHookLogger:
    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(AgentInitializedEvent, self.on_agent_initialized)
        registry.add_callback(BeforeInvocationEvent, self.on_before_invocation)
        registry.add_callback(AfterInvocationEvent, self.on_after_invocation)
        registry.add_callback(MessageAddedEvent, self.on_message_added)
        registry.add_callback(BeforeToolCallEvent, self.on_before_tool_call)
        registry.add_callback(AfterToolCallEvent, self.on_after_tool_call)
        registry.add_callback(BeforeModelCallEvent, self.on_before_model_call)
        registry.add_callback(AfterModelCallEvent, self.on_after_model_call)

    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        print(f"\n >>> Agent initialized: {event.agent.name}")

    def on_before_invocation(self, event: BeforeInvocationEvent) -> None:
        print(f"\n >>> Before invocation: {len(event.agent.messages)} message(s)")

    def on_after_invocation(self, event: AfterInvocationEvent) -> None:
        print(f"\n >>> After invocation: result={event.result}")

    def on_message_added(self, event: MessageAddedEvent) -> None:
        role = event.message.get("role", "unknown")
        print(f"\n >>> Message added ({role}): {message_to_text(event.message)}")

    def on_before_tool_call(self, event: BeforeToolCallEvent) -> None:
        print(f"\n >>> Before tool call: {event.tool_use['name']}")

    def on_after_tool_call(self, event: AfterToolCallEvent) -> None:
        if event.exception:
            print(f"\n >>> After tool call: {event.tool_use['name']} failed: {event.exception}")
        else:
            print(f"\n >>> After tool call: {event.tool_use['name']} result={event.result}")

    def on_before_model_call(self, event: BeforeModelCallEvent) -> None:
        print(f"\n >>> Before model call: {len(event.agent.messages)} message(s)")

    def on_after_model_call(self, event: AfterModelCallEvent) -> None:
        if event.exception:
            print(f"\n >>> After model call failed: {event.exception}")
            return

        if event.stop_response:
            print(f"\n >>> After model call: {message_to_text(event.stop_response.message)}")
        else:
            print("\n >>> After model call: no response")

# Bedrock
print("\n\n ===== Amazon Nova =====")
bedrock_model = BedrockModel(
model_id="us.amazon.nova-pro-v1:0",
temperature=0.3,
streaming=True, # Enable/disable streaming
)
agent = Agent(
    model=bedrock_model,
    tools=[calculator, current_time, get_weather],
    system_prompt="You are a helpful assistant with access to tools. You should provide answers no longer than 200 symbols.",
    hooks=[AllHookLogger()],
)


query = """
What is the weather in Washington, D.C.? 
"""
agent(query)