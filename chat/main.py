from flask import Flask, session, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os
from dotenv import load_dotenv

load_dotenv()

secretKey = os.getenv("SECRET_KEY")
FE_URL = os.getenv("FE_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
socketio = SocketIO(app, cors_allowed_origins=FE_URL , cors_allowed_methods=["GET", "POST"], cors_allowed_headers="*")

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('join_community')
def join_community(data):
    user_id = data['user_id']
    community_id = data['community_id']
    if user_id and community_id:
        # TODO : Add user to community
        send(str(user_id) + ' has entered the room.', to=community_id)

@socketio.on('leave_community')
def on_leave(data):
    user_id = data['user_id']
    community_id = data['community_id']
    # TODO : Remove user from community
    send(user_id + ' has left the room.', to=community_id)

@socketio.on('message_send')
def handle_message(data):
    user_id = data['user_id']
    community_id = data['community_id']
    message = data['message']
    if user_id and community_id and message:
        # TODO : Save message to database
        emit('new_msg', {'user_id': user_id, 'community_id': community_id, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
