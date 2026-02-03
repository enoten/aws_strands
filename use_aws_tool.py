from strands import Agent
from strands_tools import use_aws, file_read
import argparse

parser = argparse.ArgumentParser(
        description="Script that adds 3 numbers from CMD"
    )
parser.add_argument("--query", required=True, type=str)

args = parser.parse_args()
if args:
    query = args.query

agent = Agent(model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
              tools=[use_aws,
                     file_read])


#1. Create DynamoDB Table
# query="""create empty dynamoDB table 'service_tickets' 
#         with partition key 'ticket_id' and 
#         sort key 'key_phrase' in us-east-1 region""" 

#2. Load JSON file and display its content
# query="""
# load file 'disk_tickets.json' from directory 'tickets_dataset' and 
# show its complete content in a table format 
# where column names are fields of json file"""

#3. Count Number of Record in DynamoDB Table
#query="""count number of records in DynamoDB table 'service_tickets' in us-east-1"""

#4. [no data type for counter] Count number of records, read JSON, enrich JSON data and push it in DynamoDB table 
# query="""count number of records in dynamodb table 'service_tickets' in us-east-1 and refer to is as rec_num. 
# then read file 'access_tickets.json', enumerate each record using ticket_id field  
# starting from rec_num + 1. 
# show result in table format where column names are names of record fields. 
# finally push updated records into dynamodb table 'service_tickets' in us-east-1"""

query="count number of records in dynamodb table 'service_tickets' in us-east-1 and refer to is as rec_num. then read file 'access_tickets.json', enumerate each record using ticket_id field starting from rec_num + 1. show result in table format where column names are names of record fields.  finally push updated records into dynamodb table 'service_tickets' in us-east-1"

#5. Count number of records, read JSON, enrich JSON data and push it in DynamoDB table 
# query="""count number of records in dynamodb table 'service_tickets' in us-east-1 and refer to is as rec_num. 
# then read file 'user_tickets.json', enumerate each record using ticket_id field of type str 
# starting from rec_num + 1 formated as string of lenth 4 with preceeding zeros. 
# show result in table format where column names are names of record fields. 
# finally push updated records into dynamodb table 'service_tickets' in us-east-1 use write batch mode to push all records at once"""

#6. Retrieve data from DynamoDB table
# query = """Query the DynamoDB table called 'service_tickets' in the us-east-1 region. Get all items for key_phrase 'grant access' and show me the results in a tabular format. use all fields in the original DynamoDB table to generate the output tabular format."""

agent(query)
