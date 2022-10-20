import click
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
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
api_url = "https://api.spotify.com"
redirect_uri = "https://localhost:8080/callback"
scope = "user-library-read"


def init():

    global token, refresh_token

    if os.path.exists(f'{home_dir}/.spotag'):
        # refresh()
        print('performing refresh')
    else:
        while True:
            response = input('Would you like to perform authorization? (y/n) ')
            if response.lower() == 'y':
                # authorize()
                print('performing auth')
                break
            elif response.lower() == 'n':
                print('Exiting...')
                exit(1)
            else:
                print('Response not understood, please try again')

    load_dotenv(f'{home_dir}/.spotag')
    token = os.getenv('SPOTIFY_TOKEN')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')


@click.group()
def spotags():
    """A CLI that manages Spotify album tags"""

# @click.option('-a', '--no-auth', is_flag=True, help='Filter out APIs with required auth')
@spotags.command()
def login():
    """Perform authorization"""

    global token, refresh_token
    spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    auth = HTTPBasicAuth(client_id, client_secret)

    def update_spotag_file():
        with open(f'{home_dir}/.spotag', 'w') as f:
            f.write(f'SPOTIFY_TOKEN={token}\n')
            f.write(f'SPOTIFY_REFRESH_TOKEN={refresh_token}\n')

    def refresh():
        r = spotify.refresh_token(token_url, refresh_token=refresh_token, auth=auth)
        update_spotag_file()

    def authorize():
        authorization_url, state = spotify.authorization_url(authorization_base_url)
        print('Please go here and authorize: ', authorization_url)
        redirect_response = input('\n\nPaste the full redirect URL here: ')
        r = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)
        update_spotag_file()



@spotags.command()
def pull():
    """Fetch albums"""

    init()


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



'''







    load_tokens()

    offset = 0

    while True:
        headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {token}'
                }
        params = {
                "limit": 1,
                "offset": offset
                }
        r = requests.get(f'{api_url}/v1/me/albums', headers=headers, params=params)
        if r.status_code != 200:
            print(f'Could not fetch albums:\n{r.text}')
            return False


def get_tokens():


'''
