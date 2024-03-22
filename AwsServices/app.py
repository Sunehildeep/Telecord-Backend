from chalice import Chalice
import boto3
from database.dynamodb import DynamoDB
from aws_services import AWSServices

app = Chalice(app_name='AwsServices')

# Calling the DynamoDB class to create the table
dynamo_resource = boto3.resource('dynamodb')
dynamo_db = DynamoDB(dynamo_resource)

# Calling the AWSServices
aws_services = AWSServices()

############################################################################################################
# Routes
############################################################################################################


@app.route('/sign-up', methods=['POST'], cors=True)
def sign_up():
    request = app.current_request
    body = request.json_body
    return dynamo_db.signUp(body)


@app.route('/login', methods=['POST'], cors=True)
def login():
    request = app.current_request
    req = dynamo_db.login(request.json_body)
    return req


@app.route('/addCommunity', methods=['PUT'], cors=True)
def index():
    request = app.current_request
    return dynamo_db.putCommunity(request.json_body)


@app.route('/searchCommunity', methods=['POST'], cors=True)
def index():
    request = app.current_request
    return dynamo_db.searchCommunity(request.json_body['Query'])


@app.route('/getCommunity/{user_name}', methods=['GET'], cors=True)
def get_community(user_name):
    return dynamo_db.getCommunity(user_name)


@app.route('/getCommunityById/{community_id}', methods=['GET'], cors=True)
def get_community_by_id(community_id):
    return dynamo_db.getCommunityById(community_id)


@app.route('/updateUserProfile', methods=['PUT'], cors=True)
def update_profile():
    request = app.current_request
    return dynamo_db.update_profile(request.json_body)


@app.route('/getUser', methods=['POST'], cors=True)
def get_user():
    request = app.current_request
    return dynamo_db.get_user(email=request.json_body['Email'])


@app.route('/searchUsers', methods=['GET'], cors=True)
def search_users(query, pageNumber):
    return dynamo_db.search_users(query, pageNumber)


@app.route('/deleteUser', methods=['DELETE'], cors=True)
def delete_user():
    request = app.current_request
    return dynamo_db.delete_user(request.json_body)


@app.route('/joinCommunity', methods=['POST'], cors=True)
def join_community():
    request = app.current_request
    return dynamo_db.join_community(request.json_body)


@app.route('/leaveCommunity', methods=['POST'], cors=True)
def leave_community():
    request = app.current_request
    return dynamo_db.leave_community(request.json_body)


@app.route('/translate', methods=['POST'], cors=True)
def translate():
    # requires a text, lang, and source lang
    request = app.current_request
    return aws_services.translate_text(request.json_body['translated_text'], request.json_body['source_lang'], request.json_body['target_lang'])


@app.route('/upload', methods=['POST'], cors=True)
def upload():
    request = app.current_request
    return aws_services.upload_file(request.json_body['file_bytes'], request.json_body['file_name'])


@app.route('/audio', methods=['POST'], cors=True)
def audio():
    request = app.current_request
    return aws_services.audio(request.json_body['text'])
