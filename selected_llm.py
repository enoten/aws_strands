from strands import Agent
from strands.models import BedrockModel
from strands.models.ollama import OllamaModel
from strands.models.llamaapi import LlamaAPIModel
from strands.models.gemini import GeminiModel
#from strands.models.llamacpp import LlamaCppModel

allowed_models = ['Nova',
                  'Gemini','Ollama']

query = """
What is the capital of the United States of America?
"""

# Bedrock
if 'Nova' in allowed_models:
    print("\n\n ===== Amazon Nova =====")
    bedrock_model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    temperature=0.3,
    streaming=True, # Enable/disable streaming
    )
    agent = Agent(model=bedrock_model)
    agent(query)

# Google Gemini
if 'Gemini' in allowed_models:
    print("\n\n ===== Google Gemini =====")
    gemini_model = GeminiModel(
    client_args={
        "api_key": "...put_your_api_key...",
    },
    model_id="gemini-2.5-flash",
    params={"temperature": 0.7}
    )
    agent = Agent(model=gemini_model)
    agent(query)

# Ollama
if 'Ollama' in allowed_models:
    print("\n\n ===== Ollama =====")
    ollama_model = OllamaModel(
    host="http://localhost:9000",
    model_id="llama3.1"
    )
    agent = Agent(model=ollama_model)
    agent(query)

# Llama API
if 'Llama' in allowed_models:
    print("\n\n ===== Llama API =====")
    llama_model = LlamaAPIModel(
        model_id="gemma3",
    )
    agent = Agent(model=llama_model)
    response = agent(query)