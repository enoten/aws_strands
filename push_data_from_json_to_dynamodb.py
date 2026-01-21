import boto3
import json

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('service_tickets')

def upload_data(file_name):
    with open(file_name) as json_file:
        items = json.load(json_file)
        
        # Use a batch writer to speed up the process
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    print("Upload complete!")

upload_data('access_tickets.json')