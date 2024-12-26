# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:46:35 2024

@author: AnirbanDas
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Credentials:
    def __init__(self):
        API_KEY = os.getenv("API_KEY")
        API_SECRET = os.getenv("API_SECRET")
        TOTP = os.getenv("TOTP")
        Z_USERNAME = os.getenv("Z_USERNAME")
        Z_PASSWORD = os.getenv("Z_PASSWORD")
        REDIRECT_URL = os.getenv("REDIRECT_URL")
        self.credentials = {
            "api_key": API_KEY,
            "api_secret": API_SECRET,
            "totp": TOTP,
            "username": Z_USERNAME,
            "password": Z_PASSWORD,
            "redirect_url": REDIRECT_URL
        }

    def get_credentials(self):
        return self.credentials


# print(API_KEY, API_SECRET, TOTP, Z_USERNAME, Z_PASSWORD)
