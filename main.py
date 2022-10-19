import click
import requests
import os
import json
import webbrowser
from dotenv import load_dotenv
import base64
from urllib.parse import urlencode

@click.group()
def spotags():
    """A CLI that manages Spotify album tags"""

# @click.option('-t', '--title', help='Name of API (matches via substring - i.e. "at" would return "cat" and "atlas".')
# @click.option('-c', '--category', help='Return only APIs from this category')
# @click.option('-a', '--no-auth', is_flag=True, help='Filter out APIs with required auth')
@spotags.command()
def login():
    """Perform authorization"""
    
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
    redirect_uri = "http://localhost:8080/callback"
    params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "user-library-read"
            }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(params))
    
    code = input('Code: ')
    
    token_headers = {
            "Authorization": "Basic " + encoded_credentials,
            "Content-Type": "application/x-www-form-urlencoded"
            }
    token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
            }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    token = r.json()["access_token"]

@spotags.command()
def albums

if __name__ == '__main__':
    spotags(prog_name='spotags')
