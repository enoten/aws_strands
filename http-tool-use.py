from strands_tools import http_request
from strands import Agent


dog_breed_helper = Agent(
    model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    system_prompt="""
        you are a dog breed expert specializing in helping new pet parents decide what
        breed meets their lifestyles. your expertise covers dog behavior, dog training,
        basic veterinary care and dog breed standards.dog_breed_helper

        when givint recommendations:
        1. Provide both benefits and challenges of owing that breed
        2. Only provide 3 recommendations at a time
        3. Give examples when necessary
        4. Avoid jargon, but indicate when complex concepts are important

        Your goal is to help pet parents make an informed decision about their choice in a dog.
    """
    tools=[http_request]
)

query = """
Answer these questions:
1. which dog should I adopt as a first time owner if I have an office job m-f 9-5, like to hike on
weekends and don't know much about training?
2. search wikipedia for the top 5 most popular dog breeds of the last 5 years
"""

response = dog_breed_helper(query)