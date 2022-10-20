import click
import requests
import os
import json
import webbrowser
from dotenv import load_dotenv
import base64
from urllib.parse import urlencode
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth


load_dotenv()
home_dir = os.getenv('HOME')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
api_url = "https://api.spotify.com"
redirect_uri = "https://localhost:8080/callback"
scope = "user-library-read"

@click.group()
def spotags():
    """A CLI that manages Spotify album tags"""

# @click.option('-a', '--no-auth', is_flag=True, help='Filter out APIs with required auth')
@spotags.command()
def login():
    """Perform authorization"""
    
    spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = spotify.authorization_url(authorization_base_url)
    
    print('Please go here and authorize: ', authorization_url)
    redirect_response = input('\n\nPaste the full redirect URL here: ')

    auth = HTTPBasicAuth(client_id, client_secret)

    token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)
    with open(f'{home_dir}/.spotag', 'w') as f:
        f.write(f'SPOTIFY_TOKEN={token["access_token"]}\n')
        f.write(f'SPOTIFY_REFRESH_TOKEN={token["refresh_token"]}\n')


@spotags.command()
def albums():
    """List albums"""

    load_dotenv(f'{home_dir}/.spotag')
    token = os.getenv('SPOTIFY_TOKEN')
    headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
            }
    params = {
            "limit": 2
            }
    r = requests.get(f'{api_url}/v1/me/albums', headers=headers, params=params)

    print(r.text)


if __name__ == '__main__':
    spotags(prog_name='spotags')
