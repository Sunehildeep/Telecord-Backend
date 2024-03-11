from flask import Flask, session
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
        join_room(community_id)
        send(str(user_id) + ' has entered the room.', to=community_id)
        print('Client joined community: ' + str(data['community_id']))

@socketio.on('leave_community')
def on_leave(data):
    user_id = data['user_id']
    community_id = data['community_id']
    leave_room(community_id)
    send(user_id + ' has left the room.', to=community_id)

@socketio.on('message_send')
def handle_message(data):
    user_id = data['user_id']
    community_id = data['community_id']
    message = data['message']
    print('received message: ' + str(data))
    if user_id and community_id and message:
        emit('new_msg', {'user_id': user_id, 'community_id': community_id, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
