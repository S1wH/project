import eel
import pyglet
import sqlite3
from random import randint

eel.init("web")
connection = sqlite3.connect('songs_db.db')


def choose_random_song(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM songs_db')
    amount_songs = len(cursor.fetchall())
    random_id = randint(1, amount_songs)
    cursor.execute(f'SELECT path FROM songs_db WHERE id={random_id}')
    songs = cursor.fetchall()
    return songs[-1][-1]


def play_song(path):
    song_path = choose_random_song(connection)
    song = pyglet.media.load(song_path)
    song.play()
    pyglet.app.run()


def main():
    eel.init("web")
    connection = sqlite3.connect('songs_db.db')
    eel.start('home.html', size=(700, 400))
