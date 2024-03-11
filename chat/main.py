from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

load_dotenv()

secretKey = os.getenv("SECRET_KEY")
FE_URL = os.getenv("FE_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
socketio = SocketIO(app, cors_allowed_origins=FE_URL , cors_allowed_methods=["GET", "POST"], cors_allowed_headers="*")

@socketio.on('message_send')
def handle_message(data):
    print('received message: ' + data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
