from strands import Agent
from strands_tools import calculator

agent = Agent(model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
              tools=[calculator])
agent("What is the square root of 1764")