from pydantic import BaseModel, Field
from strands import Agent
from strands.models import BedrockModel
from typing import List, Optional

class ProductAnalysis(BaseModel):
    """Analyze product information from text."""
    name: str = Field(description="Product name")
    category: str = Field(description="Product category")
    price: float = Field(description="Price in USD")
    features: List[str] = Field(description="Key product features")
    rating: Optional[float] = Field(description="Customer rating 1-5", ge=1, le=5)

bedrock_model = BedrockModel()

agent = Agent(model=bedrock_model)

result = agent.structured_output(
    ProductAnalysis,
    """
    Analyze this product: The UltraBook Pro is a premium laptop computer
    priced at $1,299. It features a 15-inch 4K display, 16GB RAM, 512GB SSD,
    and 12-hour battery life. Customer reviews average 4.5 stars.
    """
)

print(f"Product: {result.name}")
print(f"Category: {result.category}")
print(f"Price: ${result.price}")
print(f"Features: {result.features}")
print(f"Rating: {result.rating}")