import DBcm

config = {
    'host': 'localhost',
    'user': 'topuser',
    'password': 'toppasswrd',
    'database': 'topscoreDB',
}

def add_to_scores(name, time, attempts):
    with DBcm.UseDatabase(config) as cursor:
        SQL = "insert into leaderboard (name, time, attempts) values (%s,%s,%s)"
        cursor.execute(SQL, (name,time, attempts))

def sort_order(line):
    return line[-1], line[1]

def get_sorted_leaderboard():
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select name, time, attempts from leaderboard order by attempts, time"
        cursor.execute(SQL)
        data = cursor.fetchall()
    return data