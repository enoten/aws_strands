import asyncio
from strands.experimental.bidi import BidiAgent, BidiAudioIO
from strands.experimental.bidi.models import BidiNovaSonicModel
from strands.experimental.bidi.io import BidiTextIO
from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent
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
    system_prompt="You are a helpful assistant with access to tools. You should provide answers no longer than 200 symbols.",
)


def before_tool_callback(event: BeforeToolCallEvent) -> None:
    print(f">>> Tool called: {event.tool_use['name']}")


def after_tool_callback(event: AfterToolCallEvent) -> None:
    print(f">>> Tool finished: {event.tool_use['name']}")


agent.hooks.add_callback(BeforeToolCallEvent, before_tool_callback)
agent.hooks.add_callback(AfterToolCallEvent, after_tool_callback)

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