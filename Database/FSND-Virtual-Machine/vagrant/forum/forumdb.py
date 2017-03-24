#
# Database access functions for the web forum.
#

import time
import psycopg2

## Get posts from database.
def GetAllPosts():

    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    query = "Select time, content from posts order by time desc"
    cursor.execute(query)
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in cursor.fetchall()]
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):

    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    cursor.execute("INSERT INTO posts (content) VALUES (%s)", (content ,))
    db.commit()
    db.close()


