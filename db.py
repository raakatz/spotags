import sqlite3

db_file = "albums.db"

sql_insert_album = """ INSERT INTO albums(uri,name,artist,active)
                    VALUES(?,?,?,?); """

sql_select_all = "SELECT * FROM albums;"

sql_get_tags = "SELECT tags FROM albums WHERE active=1;"

sql_get_active_uris = "SELECT uri FROM albums WHERE active=1"
sql_get_inactive_uris = "SELECT uri FROM albums WHERE active=0"

sql_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
                                uri text PRIMARY KEY,
                                name text NOT NULL,
                                artist text NOT NULL,
                                tags text,
                                active integer NOT NULL
                            ); """

def create_connection():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() == None:
        cur.execute(sql_albums_table)
    return conn

def all_tags(conn):
    tags = set()
    cur = conn.cursor()
    for tags_string in cur.execute(sql_get_tags):
        tags_list = tags_string[0].split(',')
        tags_set = set(tags_list)
        tags = tags.union(tags_set)
    return tags

def get_uris(conn):
    
    active_uris = set()
    inactive_uris = set()

    cur = conn.cursor()

    for uri in cur.execute(sql_get_active_uris):
        active_uris.add(uri)
    for uri in cur.execute(sql_get_inactive_uris):
        inactive_uris.add(uri)

    return active_uris, inactive_uris

"""
def insert_new_albums():

def tag_album():

def prune_album():

def activate_album():

def get_albums():

def get_album_tags():
"""
