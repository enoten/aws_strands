from strands import Agent
from strands.models import BedrockModel

bebedrock_model = BedrockModel(
    model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature = 0.3,
    top_p=0.8,
    streaming=True
)

agent = Agent(
    model = bedrock_model
)