# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:52:14 2024

@author: AnirbanDas
"""
import time
from urllib.parse import urlparse, parse_qs

from flask import request
from kiteconnect import KiteConnect
from config.credentials import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyotp import TOTP

from models.session import ZSession

# Fetch credentials from environment
credentials = Credentials()
api_key, api_secret, totp, username, password, redirect_url = credentials.get_credentials().values()
kite = None

def login_to_kite():
    print("Starting headless browser for login...")

    # Configure headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        login_url = f"https://kite.zerodha.com/connect/login?api_key={api_key}&redirect_url={redirect_url}"
        print(login_url)
        driver.get(login_url)

        print("Logging in...")
        time.sleep(3)

        # Fill in login credentials (replace with your credentials)
        driver.find_element("id", "userid").send_keys(username)
        driver.find_element("id", "password").send_keys(password)
        driver.find_element("css selector", "button[type=submit]").click()

        # Wait for PIN entry page to load
        time.sleep(5)
        print("Generating PIN ...")

        totp_pin = TOTP(totp)
        print(totp_pin.now())
        # Enter PIN (replace with your actual PIN)
        driver.find_element("id", "userid").send_keys(totp_pin.now())
        driver.find_element("css selector", "button[type=submit]").click()

        # Wait for redirection to complete
        print("Waiting for redirection...")
        time.sleep(5)

        # print(driver.current_url)
        # parsed_url = urlparse(driver.current_url)
        # # Extract query params
        # query_params = parse_qs(parsed_url.query)
        # request_token = query_params.get('request_token',[None])[0]
        # print(f"Request Token: {request_token}")
        # generate_kite_session(request_token)
        print("Login completed. Waiting for request token capture...")

    except Exception as e:
        print(f"Error during login: {e}")
    finally:
        driver.quit()

def generate_kite_session(request_token):
    if request_token:
        # Step 3: Generate access token
        global kite
        kite = KiteConnect(api_key=api_key)
        try:
            data = kite.generate_session(
                request_token=request_token, api_secret=api_secret
            )
            access_token = data["access_token"]
            login_time = data["login_time"]

            print(data)
            print("Access token generated:", access_token)

            kite.set_access_token(access_token)
            ZSession(request_token, access_token, login_time).add()
            # return f"Access token generated: {access_token}"
            # return request_token
        except Exception as e:
            print("Error generating access token:", e)
            # return "Error generating access token"
            # return None
    else:
        print("Request token not found!")
        # return None

def logout_kite(access_token):
    global kite
    kite = KiteConnect(api_key=api_key)
    if kite:
        kite.invalidate_access_token(access_token)
        ZSession.invalidate_session(access_token)


# login_to_kite()

