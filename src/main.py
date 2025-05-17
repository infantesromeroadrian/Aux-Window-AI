from flask import Flask
from flask_socketio import SocketIO

from controllers.transcription_controller import register_transcription_routes
from utils.config import Config

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config.from_object(Config)
socketio = SocketIO(app)

# Register routes
register_transcription_routes(app, socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 