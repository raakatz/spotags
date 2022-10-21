import sqlite3

def db_init():

def create_table():

def insert_new_albums():

def tag_album():

def prune_album():

def activate_album():

def get_albums():

def get_album_tags():

def all_tags():
    db_init()

all_tags = set()


db_file = "albums.db"

conn = sqlite3.connect(db_file)

cur = conn.cursor()

sql_albums_table = """ CREATE TABLE IF NOT EXISTS albums (
                                        uri text PRIMARY KEY,
                                        name text NOT NULL,
                                        artist text NOT NULL,
                                        tags text,
                                        active integer NOT NULL
                                    ); """

sql_insert_album = """ INSERT INTO albums(uri,name,artist,tags,active)
                    VALUES(?,?,?,?,?); """


sql_select_all = "SELECT * FROM albums;"

sql_get_tags = "SELECT tags FROM albums WHERE active=1;"

album1 = ('spotify:abc:123', 'blackwater', 'opeth', 'metal,black', 1)
album2 = ('spotify:def:456', 'heritage', 'opeth', 'metal,modern', 1)

albums = [album1, album2]

cur.execute(sql_albums_table)

for album in albums:
    try:
        cur.execute(sql_insert_album, album)
    except:
        continue

conn.commit()
'''
for album in cur.execute(sql_select_all):
    print(album)
'''
for tags_string in cur.execute(sql_get_tags):
    tags_list = tags_string[0].split(',')
    tags_set = set(tags_list)
    all_tags = all_tags.union(tags_set)

print(all_tags)

conn.close()

