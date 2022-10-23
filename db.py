import sqlite3

db_file = "albums.db"

sql_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
                                uri text PRIMARY KEY,
                                name text NOT NULL,
                                artist text NOT NULL,
                                tags text,
                                active integer NOT NULL
                            ); """


sql_get_tags = "SELECT tags FROM albums WHERE active=1 ORDER BY artist;"

sql_get_album_tags = "SELECT tags FROM albums WHERE uri=?;"

sql_get_active_uris = "SELECT uri FROM albums WHERE active=1"

sql_get_inactive_uris = "SELECT uri FROM albums WHERE active=0"

sql_insert_albums = "INSERT INTO albums(uri,name,artist,active) VALUES(?,?,?,1);"

sql_orphan_albums = "UPDATE albums SET active=0 WHERE uri=?"

sql_activate_albums = "UPDATE albums SET active=1 WHERE uri=?" 

sql_set_tags = "UPDATE albums SET tags=? WHERE uri=?"

sql_select_all = "SELECT uri,artist,name,tags FROM albums ORDER BY artist;" 

sql_select_active = "SELECT uri,artist,name,tags FROM albums WHERE active=1 ORDER BY artist;"

sql_select_all_with_wanted_tags = """ SELECT uri,artist,name,tags
                                    FROM albums
                                    WHERE uri in ({0})
                                    ORDER BY artist; """

sql_select_active_with_wanted_tags = """ SELECT uri,artist,name,tags
                                    FROM albums
                                    WHERE active=1 AND uri in ({0})
                                    ORDER BY artist; """

sql_get_empty_tags = "SELECT uri,name,artist FROM albums WHERE tags IS NULL ORDER BY artist;"

def create_connection():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() == None:
        cur.execute(sql_albums_table)
    return conn

def set_tags(conn, uri_tags, many=False):
    cur = conn.cursor()
    if many:
        cur.executemany(sql_set_tags, uri_tags)
    else:
        cur.execute(sql_set_tags, uri_tags)

def all_tags(conn, uri=None):
    tags = set()
    cur = conn.cursor()

    if uri != None:
        query = sql_get_album_tags
        res = cur.execute(query, uri)
    else:
        query = sql_get_tags
        res = cur.execute(query)
    for tags_string in res:
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

def get_albums(conn, uris=None, fetch_with_tags=False, fetch_all=False, get_empty=False):
    cur = conn.cursor()
    if fetch_with_tags:
        if fetch_all:
            albums = cur.execute(sql_select_all_with_wanted_tags.format(', '.join('?' for _ in uris)), uris)
        else:
            albums = cur.execute(sql_select_active_with_wanted_tags.format(', '.join('?' for _ in uris)), uris)
    elif fetch_all:
        albums = cur.execute(sql_select_all)
    elif get_empty:
        albums = cur.execute(sql_get_empty_tags)
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

