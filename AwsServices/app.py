from chalice import Chalice
import boto3
from database.dynamodb import DynamoDB

app = Chalice(app_name='AwsServices')

# Calling the DynamoDB class to create the table
dynamo_resource = boto3.resource('dynamodb')
dynamo_db = DynamoDB(dynamo_resource)

@app.route('/addCommunity', methods=['PUT'], cors=True)
def index():
    request = app.current_request
    dynamo_db.putCommunity(request.json_body)
    return {'message': 'Community added successfully!'}

@app.route('/getCommunity/{user_name}', methods=['GET'], cors=True)
def get_community(user_name):
    return dynamo_db.getCommunity(user_name)

