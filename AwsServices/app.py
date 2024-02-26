from chalice import Chalice
import boto3
from database.dynamodb import DynamoDB

app = Chalice(app_name='AwsServices')

# Calling the DynamoDB class to create the table
dynamo_resource = boto3.resource('dynamodb')
DynamoDB(dynamo_resource)

@app.route('/', methods=['GET'], cors=True)
def index():
    return {'hello': 'world'}