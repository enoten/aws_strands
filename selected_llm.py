from strands import Agent
from strands.models import BedrockModel
from strands.models.gemini import GeminiModel
from strands.models.ollama import OllamaModel

from dotenv import load_dotenv
load_dotenv()

import os
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

allowed_models = ['Nova',
                  'Gemini','Ollama']

query = """
What is the capital of the United States of America?
"""

print("\n\n ===== Direct Reference to the Model =====")
agent = Agent(model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
agent(query)

# Bedrock
if 'Nova' in allowed_models:
    print("\n\n ===== Amazon Nova =====")

    bedrock_model = BedrockModel(
                                  model_id="us.amazon.nova-pro-v1:0",
                                  temperature=0.3,
                                  streaming=True, # Enable/disable streaming
                                )
    print(f"Selected model {bedrock_model.get_config()}\n")
    agent = Agent(model=bedrock_model)
    agent(f"Response: {agent(query)}")

# Google Gemini
if 'Gemini' in allowed_models:
    print("\n\n ===== Google Gemini =====")

    gemini_model = GeminiModel(
                                client_args={
                                    "api_key": GOOGLE_API_KEY,
                                },
                                model_id="gemini-2.5-flash",
                                params={"temperature": 0.7}
                              )
    print(f"Selected model {gemini_model.get_config()}\n")
    agent = Agent(model=gemini_model)
    agent(f"Response: {agent(query)}")

# Ollama
if 'Ollama' in allowed_models:
    print("\n\n ===== Ollama =====")
    
    ollama_model = OllamaModel(
                                host="http://localhost:9000",
                                #model_id="llama3.1"
                                model_id="gemma3:4b"
                                #model_id="qwev3:4b"
                              )
    print(f"Selected model {ollama_model.get_config()}\n")
    agent = Agent(model=ollama_model)
    (f"Response: {agent(query)}")

print('\n')
