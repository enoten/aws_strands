from strands import Agent
from strands_tools import use_aws, file_read, file_write
import sys
import argparse

parser = argparse.ArgumentParser(
        description="Script that adds 3 numbers from CMD"
    )
parser.add_argument("--query", required=True, type=str)

agent = Agent(model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
              tools=[use_aws,
                     file_read, 
                     file_write])

#query = "List the s3 buckets in my account"

#query = "Query the DynamoDB table called 'service_tickets' in the us-east-1 region. Get all items for key_phrase 'grant access' and show me the results in a readable format."

#query="load file 'disk_tickets.json' and show its complete content in a table format where column names are fields of json file"

#query="create empty dynamoDB table 'service_tickets' with partition key 'ticket_id' and sort key 'key_phrase' in us-east-1 region" 

#query="count number of records in dynamodb table 'service_tickets' in us-east-1"

query = "show me content of 'disk_tickets.json' file"

args = parser.parse_args()
if args:
    query = args.query

#if sys.argv[1]:
#    query = sys.argv[1]

agent(query)