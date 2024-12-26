# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:53:37 2024

@author: AnirbanDas
"""

import time
import os
from threading import Thread
from flask import Flask, request
from kiteconnect import KiteConnect
from dotenv import load_dotenv
from core.z_auth import login_to_kite, capture_request_token
import logging

load_dotenv()
PORT = os.getenv('PORT')
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask app
app = Flask(__name__)

# Global variable to store the request token
# request_token = None


# @app.route("/")
# def login_to_kite():
#     login_to_kite()

@app.route('/callback', methods=['GET'])
def callback():
    app.logger.debug("Callback endpoint hit")
    request_token = request.args.get("request_token")
    app.logger.debug(f"REQ TOKEN: {request_token}")
    print(f"Got {request_token}")

# capture_request_token()


if __name__ == "__main__":
    # Start the Flask server in separate thread
    server_thread = Thread(
        target=lambda: app.run(port=PORT, debug=False, use_reloader=False)
    )
    server_thread.start()

    login_to_kite()

    # Wait for server thread to complete
    server_thread.join()
