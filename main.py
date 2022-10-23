import click
import requests
import json
from tokens import init
import db
from helpers import setify_tags, prompt_before_exit


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
    uris_albums_to_activate = inactive_uris.intersection(pulled_uris)
    
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
    
    print(f'{len(new_albums)} new albums were added')
    print(f'{len(albums_to_orphan)} albums were archived')
    print(f'{len(albums_to_activate)} were renewed from archive')
    

@spotags.command()
def tags():
    """List all used tags"""
    
    conn = db.create_connection()
    tags = db.all_tags(conn)
    conn.close()

    if len(tags) == 0:
        print('No used tags')
    else:
        for tag in tags:
            print(tag)


@click.option('--empty', is_flag=True)
@click.option('-a', '--album', type=str)
@click.option('-t', '--tags', type=str)
@click.option('--overwrite', is_flag=True)
@click.option('--delete', is_flag=True)
@spotags.command()
def tag(album, tags, overwrite, delete, empty):
    """Tag an album"""
    
    if album and not tags and not delete and not empty:
        print('No tags were specified')
        exit(1)

    elif delete and overwrite and not empty:
        
        prompt_before_exit('WARNING, overwriting! Continue? (y/n) ')

        conn = db.create_connection()

        db.set_tags(conn, tuple((None, album)))

        conn.commit()
        conn.close()


    elif empty:

        conn = db.create_connection()

        albums = db.get_albums(conn, get_empty=True)

        uris_tags_list = list()

        for album in albums:
            res = input(f'Please enter new tags for {album[2]} - {album[1]} ("exit" to exit)\n')
            
            wanted_tags = setify_tags(res)

            if wanted_tags == set(('exit',)):
                prompt_before_exit('Save changes? (y/n) ')
                break
            else:
                wanted_tags = ','.join(wanted_tags)
            
            uris_tags_list.append(tuple((wanted_tags, album[0])))

        db.set_tags(conn, uris_tags_list, many=True)

        conn.commit()
        conn.close()

    else:

        wanted_tags = setify_tags(tags)

        if overwrite:

            prompt_before_exit('WARNING, overwriting! Continue? (y/n) ')

            conn = db.create_connection()

            final_tags_str = ','.join(wanted_tags)
            
            db.set_tags(conn, tuple((final_tags_str, album)))

        else:
            
            conn = db.create_connection()

            current_tags_set = db.all_tags(conn, tuple((album,)))
            
            final_tags = wanted_tags.union(current_tags_set)
            
            final_tags_str = ','.join(final_tags)
            
            db.set_tags(conn, tuple((final_tags_str, album)))
        
        conn.commit()
        conn.close()


@click.option("-t", "--tags", help="Search by tags, comma-seperated list")
@click.option("--archived", is_flag=True, help="Show archived")
@spotags.command()
def albums(tags, archived):
    """List albums"""

    def get_uris_with_tags(wanted_tags, all_albums):
        uri_list = list()
        for album in all_albums:
            if album[3] != None:
               album_tags = setify_tags(album[3])
               if wanted_tags.issubset(album_tags):
                   uri_list.append(album[0])
        return uri_list

    conn = db.create_connection()
    
    if tags != None:
        
        wanted_tags = setify_tags(tags)

        if archived:
            
            all_albums = db.get_albums(conn, fetch_all=True)

            uris_with_wanted_tags = get_uris_with_tags(wanted_tags, all_albums)

            albums = db.get_albums(conn, uris=uris_with_wanted_tags, fetch_with_tags=True, fetch_all=True)

        else:

            all_albums = db.get_albums(conn)
            
            uris_with_wanted_tags = get_uris_with_tags(wanted_tags, all_albums)

            albums = db.get_albums(conn, uris=uris_with_wanted_tags, fetch_with_tags=True) 


    elif archived:
        albums = db.get_albums(conn, fetch_all=True)
    else:
        albums = db.get_albums(conn)

    conn.close()

    for album in albums:
        print(f'{album[0]}\t{album[1]:<50}{album[2]:<50}{album[3]}')


if __name__ == '__main__':
    spotags(prog_name='spotags')


