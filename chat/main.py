from flask import Flask, session, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os
from dotenv import load_dotenv

load_dotenv()

secretKey = os.getenv("SECRET_KEY")
FE_URL = os.getenv("FE_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
socketio = SocketIO(app, cors_allowed_origins=FE_URL, cors_allowed_methods=[
                    "GET", "POST"], cors_allowed_headers="*")


@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('join_community')
def join_community(CommunityId):
    print('User joined community', str(CommunityId))
    join_room(str(CommunityId))


@socketio.on('leave_community')
def on_leave(CommunityId):
    print('User left community', str(CommunityId))
    leave_room(str(CommunityId))


@socketio.on('message_send')
def handle_message(data):
    print('received message: ' + data['Username'])
    username = data['Username']
    community_id = data['CommunityId']
    message = data['Message']
    if username and community_id and message:
        emit('new_msg', data, room=community_id)


if __name__ == '__main__':
    socketio.run(app, debug=True)
