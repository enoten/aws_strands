from strands import Agent, tool

@tool
def fx_cross_rates(base: str,
                target: str
                #api_key: str
                ):
    """
    Fetches the current exchange rate between two currencies.

    Args:
            base: The base currency (e.g., "SGD").
            target: The target currency (e.g., "JPY").

    Returns:
            The exchange rate information as a json response,
            or None if the rate could not be fetched.
    """

    api_url =  f"http://127.0.0.1:5000/rate/{base}/{target}"
    
    response = requests.get(api_url)
    if response.status_code == 200:
            #print(response.__dict__)
            return response.json() 
    else:
            return {'data':None}

agent = Agent(
              model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
              tools=[fx_cross_rates])

response = agent("what is a cross rate for USD and EUR?"
"")