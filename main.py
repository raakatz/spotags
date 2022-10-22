import click
import requests
import json
from tokens import init
import db

@click.group()
def spotags():
    """A CLI that manages Spotify album tags"""


@spotags.command()
def pull():
    """Fetch albums"""

    token = init()
    
    offset = 0
    pulled_albums = set()
    pulled_uris = set()

    while True:
        headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {token}'
                }
        params = {
                "limit": 50,
                "offset": offset
                }
        r = requests.get('https://api.spotify.com/v1/me/albums', headers=headers, params=params)
        r = r.json()

        for item in r["items"]:
            album_name = item["album"]["name"]
            album_uri = item["album"]["uri"]
            album_artist = item["album"]["artists"][0]["name"]
            pulled_albums.add(tuple((album_uri, album_name, album_artist)))
            
        if r["next"] == None:
            break
        else:
            offset += 50

    for album in pulled_albums:
        pulled_uris.append(album[0])

    conn = db.create_connection()

    active_uris, inactive_uris = db.get_uris(conn)
    all_existing_uris = active_uris.union(inactive_uris)
    new_albums = pulled_uris.difference(all_existing_uris)

    

    """
    compare lists, make new_albums, common_albums, orphan_albums

    for album in new_albums,
        add album to db
    for album in common_albums,
        mark active=1
    for album in orphan_albums,
        mark active=0
    """

    """
    if rows with empty tags,
    ask to start tagging all active with no tags by running tag()
    """
    conn.close()
    
@spotags.command()
def tags():
    """List all used tags"""
    
    conn = db.create_connection()
    tags = db.all_tags(conn)
    print(tags)
    conn.close()


@spotags.command()
def tag():
    """Tag an album"""

    """
    tag by uri
    if run without flag, tag all that have empty tags
    if no --overwrite, only append tags
    """

@spotags.command()
def albums():
    """List albums"""

    """
    SELECT uri,artist,name,tags FROM albums WHEN active=1

    sort by artist
    --tags
    """

if __name__ == '__main__':
    spotags(prog_name='spotags')


