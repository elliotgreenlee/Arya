import base64
import requests
import webbrowser
import threading
from flask import Flask, request
from Utils.utils import load_json
import subprocess

kroger_credentials_path = 'Credentials/kroger_client.json'
credentials = load_json(kroger_credentials_path)

# Configuration
CLIENT_ID = credentials['client_id']
CLIENT_SECRET = credentials['client_secret']
REDIRECT_URI = 'http://localhost:8081/callback'
AUTH_URL = "https://api.kroger.com/v1/connect/oauth2/authorize"
TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"
PROFILE_URL = "https://api.kroger.com/v1/identity/profile"

# Flask app to handle redirects
app = Flask(__name__)

# Global variable to store access tokens
access_token = None


@app.route('/')
def index():
    return "OAuth flow initiated. Please complete the authentication in the opened popup window."


@app.route('/callback')
def callback():
    # Step 2: Extract the authorization code from the query string
    authorization_code = request.args.get('code')
    if not authorization_code:
        return "Authorization code not found!", 400

    # Step 3: Exchange the authorization code for an access token
    mycredentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(mycredentials.encode()).decode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
    }
    token_response = requests.post(TOKEN_URL, headers=headers, data=data)

    if token_response.status_code != 200:
        return f"Error obtaining access token: {token_response.text}", 400

    global access_token
    access_token = token_response.json().get('access_token')

    # Step 4: Save the token to a file
    with open('Credentials/kroger_user_token.json', 'w') as f:
        f.write(token_response.text)

    return


def open_popup(url):
    # Open a popup window using subprocess for macOS/Linux/Windows
    if subprocess.run(["which", "xdg-open"]).returncode == 0:
        subprocess.run(["xdg-open", url])  # Linux
    elif subprocess.run(["which", "open"]).returncode == 0:
        subprocess.run(["open", url])  # macOS
    else:
        webbrowser.open(url)  # Fallback for Windows or unknown systems


def start_oauth_flow():
    # Step 1: Generate the authorization URL
    auth_url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=profile.compact"
    )

    # Open the authorization URL in a popup window
    print(f"Opening the popup window for OAuth flow at: {auth_url}")
    threading.Thread(target=open_popup, args=(auth_url,)).start()

    # Start the Flask server to handle the callback
    print("Waiting for user to complete authentication...")
    app.run(host='localhost', port=8081, use_reloader=False)


if __name__ == "__main__":
    start_oauth_flow()
