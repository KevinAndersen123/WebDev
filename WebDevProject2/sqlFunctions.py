#author Kevin Andersen
import DBcm

config = { 
    'host': 'localhost',
    'user': 'gameuser',
    'password': 'gameuserpassword',
    'database': 'gameReviewDB',
}

def add_to_titles(name, studio, year, genre, platform):
    with DBcm.UseDatabase(config) as cursor:  
        SQL = "insert into titles (name, studio, year, genre, platform) values (%s, %s, %s ,%s ,%s)"
        cursor.execute(SQL, (name, studio, year, genre, platform))
        
def add_to_review(game_id, user_id, like, played, owned, rating, comment):
    with DBcm.UseDatabase(config) as cursor:
        SQL = "insert into review (game_id, user_id, like, played, owned, rating, comment) values (%s, %s, %s ,%s ,%s , %s, %s, %s)"
        cursor.execute(SQL, (game_id, user_id, like, played, owned, rating, comment))