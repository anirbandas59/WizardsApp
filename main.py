# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:53:37 2024

@author: AnirbanDas
"""

import time
import os
from threading import Thread
from flask import Flask, request
from dotenv import load_dotenv

from config.database_settings import DATABASE_URI
from core.z_auth import login_to_kite, generate_kite_session, logout_kite
import logging

from models import init_db, db
from models.session import ZSession

load_dotenv()
PORT = os.getenv('PORT')
logging.basicConfig(level=logging.INFO)

# Initialize the Flask app
app = Flask(__name__)
app.config["DATABASE_URI"] = DATABASE_URI


init_db(app)

# Global variable to store the request token
request_token = None

@app.route("/")
def home():
    login_to_kite()
    return "Trading bot API is running ..."

@app.route("/logout")
def logout():
    global request_token
    access_token = ZSession.get_access_token(request_token)
    print(access_token)
    logout_kite(access_token)
    return f"Logged out successfully..."

@app.route('/callback', methods=['GET'])
def callback():
    global request_token
    # app.logger.debug("Callback endpoint hit")
    request_token = request.args.get("request_token")
    if request_token is not None:
        generate_kite_session(request_token)

    app.logger.debug(f"REQ TOKEN: {request_token}")
    return f"Got token: {request_token}"


if __name__ == "__main__":
    # Start the Flask server in separate thread
    server_thread = Thread(
        target=lambda: app.run(port=PORT, debug=False)
    )
    server_thread.start()

    # login_to_kite()

    # Wait for server thread to complete
    server_thread.join()
