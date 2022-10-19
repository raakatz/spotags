import click
import requests
import os
import json
from dotenv import load_dotenv

@click.group()
def spotags():
    """A CLI that manages Spotify album tags"""

# @click.option('-t', '--title', help='Name of API (matches via substring - i.e. "at" would return "cat" and "atlas".')
# @click.option('-c', '--category', help='Return only APIs from this category')
# @click.option('-a', '--no-auth', is_flag=True, help='Filter out APIs with required auth')
@spotags.command()
def login():
    """List all cataloged APIs."""
    
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    scope = 'user-read-private user-read-email'
    params = {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": "http://localhost:8080",
            "scope": scope
            }

    response = requests.get('https://accounts.spotify.com/authorize', allow_redirects=True, params=params

if __name__ == '__main__':
    spotags()
