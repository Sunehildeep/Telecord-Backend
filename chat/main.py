from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import random
from string import ascii_uppercase
import dotenv

dotenv.load_dotenv()

secretKey = dotenv.get_key("SECRET_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = secretKey
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app, debug=True)