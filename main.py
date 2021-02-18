import eel
import sqlite3
from random import randint
import playsound
now = []
played_songs = []
result = 0


def choose_random_song(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM songs_db')
    amount_songs = len(cursor.fetchall())
    while True:
        random_id = randint(1, amount_songs + 1)
        cursor.execute(f'SELECT * FROM songs_db WHERE id={random_id}')
        song = cursor.fetchall()
        if song[0][2] not in played_songs:
            break
    played_songs.append(song[0][2])
    return song


@eel.expose
def play_song():
    connection = sqlite3.connect('songs_db.db')
    song = choose_random_song(connection)
    name = song[0][1]
    artist = song[0][2]
    song_path = song[0][5]
    playsound.playsound(song_path, False)
    now.append(name + artist)
    print(name + artist)


@eel.expose
def check_song(string):
    global result
    answer = string.lower()
    correct_answer = now[0].lower()
    now.pop(0)
    answer = ''.join(answer.split())
    correct_answer = ''.join(correct_answer.split())
    correct_dict = {}
    for i in range(len(correct_answer)):
        if correct_answer[i] not in correct_dict.keys():
            correct_dict[correct_answer[i]] = 1
        else:
            correct_dict[correct_answer[i]] += 1
    mistakes = 0
    if abs(len(answer) - len(correct_answer)) > 2:
        return False
    else:
        for key, value in correct_dict.items():
            if answer.count(key) != value:
                mistakes += abs(answer.find(key) - value)
    if (len(correct_answer) - mistakes) / len(correct_answer) >= 0.75:
        result += 1
        return True
    else:
        return False


@eel.expose
def check_end():
    sp = [result]
    if len(played_songs) == 10:
        sp.append(False)
    else:
        sp.append(True)
    return sp


def main():
    eel.init("web")
    eel.start('home.html', size=(700, 400))


if __name__ == '__main__':
    main()
