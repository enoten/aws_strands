import asyncio
from strands.experimental.bidi import BidiAgent, BidiAudioIO
from strands.experimental.bidi.models import BidiNovaSonicModel
from strands.experimental.bidi.io import BidiTextIO
from strands.experimental.hooks.events import (
    BidiAfterInvocationEvent,
    BidiBeforeInvocationEvent,
    BidiMessageAddedEvent,
)
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


# Create agent with tools
model = BidiNovaSonicModel()

agent = BidiAgent(
    model=model,
    tools=[calculator, current_time, get_weather],
    system_prompt="You are a helpful assistant with access to tools. You should provide answers no lonfer than 200 symbols.",
)


def message_to_text(message: dict | None) -> str:
    if not message:
        return ""

    parts = []
    for content in message.get("content", []):
        if "text" in content:
            #parts.append(content["text"])
            parts.append(str(content))
        elif "toolUse" in content:
            #parts.append(f"[tool use: {content['toolUse'].get('name', 'unknown')}]")
            parts.append(str(content))
        elif "toolResult" in content:
            parts.append(str(content))
            #parts.append("[tool result]")
        else:
            parts.append(str(content))

    return "\n".join(parts)


async def before_llm_runtime_callback(event: BidiBeforeInvocationEvent) -> None:
    print(">>> Before LLM runtime")
    print(f">>> System prompt: {event.agent.system_prompt}")


async def after_llm_runtime_callback(event: BidiAfterInvocationEvent) -> None:
    print(">>> After LLM runtime")
    print(f">>> Messages in conversation: {len(event.agent.messages)}")


async def message_added_callback(event: BidiMessageAddedEvent) -> None:
    role = event.message.get("role", "unknown")
    prompt = message_to_text(event.message)

    if role == "user":
        print(f">>> LLM input prompt: {prompt}")
    elif role == "assistant":
        print(f">>> LLM output prompt: {prompt}")
    else:
        print(f">>> Message added ({role}): {prompt}")


agent.hooks.add_callback(BidiBeforeInvocationEvent, before_llm_runtime_callback)
agent.hooks.add_callback(BidiAfterInvocationEvent, after_llm_runtime_callback)
agent.hooks.add_callback(BidiMessageAddedEvent, message_added_callback)

audio_io = BidiAudioIO()
text_io = BidiTextIO()

async def main():
    print("Start chatting with the Agent")
    try:
        # Runs indefinitely until interrupted
        await agent.run(
        inputs=[audio_io.input(), text_io.input()],
        outputs=[audio_io.output(), text_io.output()]
        )
    except asyncio.CancelledError:
        print("\nConversation cancelled by user")
    finally:
        # stop() should only be called after run() exits
        await agent.stop()

asyncio.run(main())