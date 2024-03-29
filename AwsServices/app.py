from chalice import Chalice
import boto3
from database.dynamodb import DynamoDB
from aws_services import AWSServices
import base64

app = Chalice(app_name='AwsServices')

# Calling the DynamoDB class to create the table
dynamo_db = DynamoDB()

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


@app.route('/upload', methods=['POST'], cors=True)
def upload():
    print("Request", app.current_request.json_body)
    request = app.current_request
    file_name = request.json_body['file_name']
    print("File Name", file_name)
    file_bytes = base64.b64decode(request.json_body['file_bytes'])

    print("File Bytes", file_bytes)
    return aws_services.upload_file(file_bytes, file_name)


@app.route('/audio', methods=['POST'], cors=True)
def audio():
    request = app.current_request
    return aws_services.audio(request.json_body['text'])


@app.route('/chats', methods=['POST'], cors=True)
def chats():
    request = app.current_request
    return dynamo_db.saveChat(request.json_body)


@app.route('/chats/{communityId}', methods=['GET'], cors=True)
def get_chats(communityId):
    return dynamo_db.getChats(communityId)


@app.route('/deleteCommunity', methods=['DELETE'], cors=True)
def delete_community():
    request = app.current_request.json_body
    return dynamo_db.deleteCommunity(request)


@app.route('/updateUsername', methods=['PUT'], cors=True)
def update_username():
    request = app.current_request
    return dynamo_db.update_username(request.json_body)


@app.route('/updateUserProfilePicture', methods=['PUT'], cors=True)
def update_profile_picture():
    request = app.current_request
    print("Request", request.json_body)
    return dynamo_db.update_profile_picture(request.json_body)


@app.route('/updateCommunityImage', methods=['PUT'], cors=True)
def update_community_image():
    request = app.current_request
    return dynamo_db.update_community_image(request.json_body)


@app.route('/translate', methods=['POST'], cors=True)
def translate():
    request = app.current_request
    return aws_services.translate_text(request.json_body['chats'], request.json_body['source_lang'], request.json_body['target_lang'])
