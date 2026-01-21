aws_http_request_tool

from strands import Agent
from strands.models import BedrockModel
from strands_tools import http_request

# 1. Setup the Model (requires AWS credentials configured)
# Strands supports various models; here we use Amazon Nova or Claude via Bedrock
model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0", # Or "anthropic.claude-3-5-sonnet-v2:0"
    region_name="us-east-1"
)

# 2. Define the Agent
# We include http_request in the tools list. 
# The model will autonomously decide when and how to call it.
agent = Agent(
    model=model,
    tools=[http_request],
    system_prompt=(
        "You are a helpful assistant. You have access to a local API at http://localhost:5000/. "
        "When a user asks a question that requires external data, use the http_request tool "
        "to call that endpoint with a 'text' query parameter."
    )
)

# 3. Execute a Query
user_input = "Query my local database for the status of order #1234."
response = agent(user_input)

print(f"Agent Response: {response}")