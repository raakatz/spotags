import click
import sqlite3
import requests
import os
import json
from dotenv import load_dotenv
import base64
from urllib.parse import urlencode
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth


load_dotenv()

home_dir = os.getenv('HOME')
envfile = f'{home_dir}/.spotag'
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
api_url = "https://api.spotify.com/v1"
redirect_uri = "https://localhost:8080/callback"
scope = "user-library-read"
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
auth = HTTPBasicAuth(client_id, client_secret)


def init():

    global token, refresh_token

    if os.path.exists(envfile):
        load_tokens()
        headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {token}'
                }
        r = requests.get(f'{api_url}/me', headers=headers)

        if r.status_code >= 400:
            try:
                refresh()
            except:
                authorization_request()
            finally:
                load_tokens()
    else:
        authorization_request()


def load_tokens():

    global token, refresh_token

    load_dotenv(envfile)
    token = os.getenv('SPOTIFY_TOKEN')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')


def authorization_request():

    while True:
        response = input('Would you like to perform authorization? (y/n) ')
        if response.lower() == 'y':
            authorize()
            break
        elif response.lower() == 'n':
            print('Exiting...')
            exit(1)
        else:
            print('Response not understood, please try again')


def refresh():
    
    global token, refresh_token
    
    r = spotify.refresh_token(token_url, refresh_token=refresh_token, auth=auth)

    token = r["access_token"]
    refresh_token = r["refresh_token"]
    
    update_spotag_file()
    

def authorize():

    global token, refresh_token
    
    authorization_url, state = spotify.authorization_url(authorization_base_url)
    
    print('Please go here and authorize: ', authorization_url)
    
    redirect_response = input('\n\nPaste the full redirect URL here: ')
    
    r = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)
    
    token = r["access_token"]
    refresh_token = r["refresh_token"]
    
    update_spotag_file()


def update_spotag_file():

    with open(envfile, 'w') as f:
        f.write(f'SPOTIFY_TOKEN={token}\n')
        f.write(f'SPOTIFY_REFRESH_TOKEN={refresh_token}\n')


@click.group()
def spotags():
    """A CLI that manages Spotify album tags"""


@spotags.command()
def pull():
    """Fetch albums"""

    init()

    headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
            }
    params = {
            "limit": 1,
            "offset": 0
            }
    r = requests.get(f'{api_url}/me/albums', headers=headers, params=params)
    print(r.text)

@spotags.command()
def tags():
    """List all used tags"""

@spotags.command()
def tag():
    """Tag an album"""

@spotags.command()
def albums():
    """List albums"""


if __name__ == '__main__':
    spotags(prog_name='spotags')


