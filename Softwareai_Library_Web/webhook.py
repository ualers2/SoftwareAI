# import time

# while True:
#    time.sleep(67789)


from flask import Flask,request, jsonify, render_template_string
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
import base64
import os
import io
import requests

app = Flask(__name__)
CORS(app)  
app.config['SECRET_KEY'] = 'minha_chave_secreta'

socketio = SocketIO(app, cors_allowed_origins="*")
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB, adjust as needed


logger = logging.getLogger('webhook_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    logger.info("Webhook recebido com dados: %s", data)

    socketio.emit('webhook_data', data)
    return jsonify({"status": "sucesso", "dados": data}), 200

if __name__ == '__main__':
    print("inicialized")
    socketio.run(app, host="0.0.0.0", port=4000, allow_unsafe_werkzeug=True)