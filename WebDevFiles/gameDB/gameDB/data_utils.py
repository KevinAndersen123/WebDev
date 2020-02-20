# data_utils.py - part of the Guessing Game - by Paul Barry.
# email: paul.barry@itcarlow.ie

import DBcm


config = { 
    'host': 'localhost',
    'user': 'topuser',
    'password': 'toppasswd',
    'database': 'topscoresDB',
}


def add_to_scores(name, time, attempts):
    with DBcm.UseDatabase(config) as cursor:  
        SQL = "insert into leaderboard (name, time, attempts) values (%s, %s, %s)"
        cursor.execute(SQL, (name, time, attempts))


def get_sorted_leaderboard():
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select name, time, attempts from leaderboard order by attempts, time"
        cursor.execute(SQL)
        data = cursor.fetchall()
    return [ (row[0], float(row[1]), row[2]) for row in data ]
