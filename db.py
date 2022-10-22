import sqlite3

db_file = "albums.db"

sql_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
                                uri text PRIMARY KEY,
                                name text NOT NULL,
                                artist text NOT NULL,
                                tags text,
                                active integer NOT NULL
                            ); """

sql_select_all_by_tag = "SELECT uri,artist,name,tags FROM albums WHERE tags=?;"

sql_select_all = "SELECT uri,artist,name,tags,active FROM albums;" 

sql_select_active = "SELECT uri,artist,name,tags FROM albums WHERE active=1;"

sql_get_tags = "SELECT tags FROM albums WHERE active=1;"

sql_get_album_tags = "SELECT tags FROM albums WHERE uri=?;"

sql_get_active_uris = "SELECT uri FROM albums WHERE active=1"

sql_get_inactive_uris = "SELECT uri FROM albums WHERE active=0"

sql_insert_albums = "INSERT INTO albums(uri,name,artist,active) VALUES(?,?,?,1);"

sql_orphan_albums = "UPDATE albums SET active=0 WHERE uri=?"

sql_activate_albums = "UPDATE albums SET active=1 WHERE uri=?" 

sql_set_tags = "UPDATE albums SET tags=? WHERE uri=?"


def create_connection():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() == None:
        cur.execute(sql_albums_table)
    return conn

def set_tags(conn, uri_tags):
    cur = conn.cursor()
    cur.execute(sql_set_tags, uri_tags)


def all_tags(conn, uri=None):
    tags = set()
    if uri != None:
        query = sql_get_album_tags
    else:
        query = sql_get_tags
    cur = conn.cursor()
    for tags_string in cur.execute(query, uri):
        if tags_string[0] == None:
            continue
        else:
            tags_list = tags_string[0].split(',')
            tags_set = set(tags_list)
            tags = tags.union(tags_set)
    return tags

def get_uris(conn):
    
    active_uris = set()
    inactive_uris = set()

    cur = conn.cursor()

    for uri in cur.execute(sql_get_active_uris):
        active_uris.add(uri[0])
    for uri in cur.execute(sql_get_inactive_uris):
        inactive_uris.add(uri[0])

    return active_uris, inactive_uris

def get_albums(conn, fetch_all=False, tags=None):
    cur = conn.cursor()
    if fetch_all:
        albums = cur.execute(sql_select_all, tags)
    else:
        albums = cur.execute(sql_select_active)
    return albums.fetchall()

def update_db(conn, action, albums_list):
    
    cur = conn.cursor()
    
    def perform_action(query):
        try:
            cur.executemany(query, albums_list)
        except Exception as e:
            print(f'Could not {action} albums: {e}')

    if action == "insert":
        perform_action(sql_insert_albums)
    elif action == "orphan":
        perform_action(sql_orphan_albums)
    elif action == "activate":
        perform_action(sql_activate_albums)

