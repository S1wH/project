import eel
import sqlite3
from random import randint
import playsound
sp = []


def choose_random_song(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM songs_db')
    amount_songs = len(cursor.fetchall())
    random_id = randint(1, amount_songs)
    cursor.execute(f'SELECT * FROM songs_db WHERE id={random_id}')
    song = cursor.fetchall()
    return song


@eel.expose
def play_song():
    connection = sqlite3.connect('songs_db.db')
    song = choose_random_song(connection)
    name = song[0][1]
    artist = song[0][2]
    song_path = song[0][3]
    playsound.playsound(song_path, False)
    sp.append(name + ' ' + artist)
    print(sp[0])


@eel.expose
def check_song(string):
    if string == sp[0]:
        return True
    return False


def main():
    eel.init("web")
    eel.start('home.html', size=(700, 400))


if __name__ == '__main__':
    main()
