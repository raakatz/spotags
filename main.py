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
    new_albums = list()
    albums_to_orphan = list()
    albums_to_activate = list()

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
        pulled_uris.add(album[0])

    conn = db.create_connection()

    active_uris, inactive_uris = db.get_uris(conn)
    all_existing_uris = active_uris.union(inactive_uris)
    
    uris_new_albums = pulled_uris.difference(all_existing_uris)
    uris_albums_to_orphan = active_uris.difference(pulled_uris)
    uris_albums_to_activate = inactive_uris.difference(pulled_uris)
    
    
    for album in pulled_albums:
        if album[0] in uris_new_albums:
            new_albums.append(album)

    for uri in uris_albums_to_orphan:
        albums_to_orphan.append(tuple((uri,)))

    for uri in uris_albums_to_activate:
        albums_to_activate.append(tuple((uri,)))


    db.update_db(conn, 'insert', new_albums)
    db.update_db(conn, 'orphan', albums_to_orphan)
    db.update_db(conn, 'activate', albums_to_activate)

    conn.commit()
    conn.close()

    """
    if rows with empty tags,
    ask to start tagging all active with no tags by running tag()
    """
    
@spotags.command()
def tags():
    """List all used tags"""
    
    conn = db.create_connection()
    tags = db.all_tags(conn)
    if len(tags) == 0:
        print('No used tags')
    else:
        print(tags)
    conn.close()


@spotags.command()
def tag():
    """Tag an album"""
    # TODO
    """
    tag by uri
    if run without flag, tag all that have empty tags
    if no --overwrite, only append tags
    """

@click.option("--tags", help="Search by tags, comma-seperated list")
@click.option("--archived", is_flag=True, help="Show archived")
@spotags.command()
def albums(tags, archived):
    """List albums"""
   
    # TODO --tags
    conn = db.create_connection()
    if archived:
        albums = db.get_albums(conn, True)
    else:
        albums = db.get_albums(conn)
    print(albums)
    print(len(albums))

    conn.close()

if __name__ == '__main__':
    spotags(prog_name='spotags')


