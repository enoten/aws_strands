from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Count words in text.

    This docstring is used by the LLM to understand the tool's purpose.
    """
    return len(text.split())

agent = Agent(
              model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
              tools=[word_count])

response = agent("How many words are in the following sentense: I love pizza"
"")