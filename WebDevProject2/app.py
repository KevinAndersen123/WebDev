#author Kevin Andersen
from flask import Flask, render_template, request, session

import random
import DBcm

app = Flask(__name__)

config = { 
    'host': 'localhost',
    'user': 'gameuser',
    'password': 'gameuserpassword',
    'database': 'gameReviewDB',
}

@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html",the_title = "LOGIN")

#displays the games
@app.route("/titles")
def titles():
    with DBcm.UseDatabase(config) as cursor: 
        SQL = "select titles.id, titles.name, titles.game_studio, titles.release_year, genre.name, platform.name,titles.likes, titles.dislikes from titles, genre, platform where titles.genre = genre.id and titles.platform = platform.id "
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("viewTitles.html", the_data = data)

@app.route("/writeReview")
def writeReview():
    return render_template("writeReview.html")

#updates the titles and gets the new titles data from the database and sends to the view titles page
@app.route("/submitReview", methods=["POST"])
def submitReview():
    createReview(session["gameID"],0,request.form["Like/Dislike"],request.form["played"],request.form["ownership"],request.form["Rating"],request.form["comment"])
    #updates titles likes
    with DBcm.UseDatabase(config) as cursor:
        SQL = "update titles set likes = (select count(*) from review where review.game_id = 1  && review.liked = 1) where id =" + session["gameID"]
        cursor.execute(SQL)
    #updates titles dislikes
    with DBcm.UseDatabase(config) as cursor:
        SQL = "update titles set dislikes = (select count(*) from review where review.game_id = 1 && review.liked = 2 ) where id =" + session["gameID"]
        cursor.execute(SQL)
        
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select titles.id, titles.name, titles.game_studio, titles.release_year, genre.name, platform.name,titles.likes, titles.dislikes from titles, genre, platform where titles.genre = genre.id and titles.platform = platform.id "
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("viewTitles.html", the_data = data)

#displays the games reviews and comments based on its game id
@app.route("/gameDetails", methods=["POST"])
def gameDetails():
    session["gameID"] = request.form["gameID"]
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select * from review where review.game_id = " + session["gameID"]
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("gameDetails.html", the_data = data)

#gets the genre data to use for the dropdown to make a new game
@app.route("/insertGamePage")
def insertGamePage():
     with DBcm.UseDatabase(config) as cursor:
        SQL = "select * from genre"
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("newGame.html", the_data = data)

#creates new game then displays the new titles
@app.route("/insertNewGame" , methods=["POST"])
def insertNewGame():
    createGame(request.form["GameName"],request.form["ReleaseYear"],request.form["GameStudio"],request.form["Genre"],request.form["Platform"]) 
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select titles.id, titles.name, titles.game_studio, titles.release_year, genre.name, platform.name,titles.likes, titles.dislikes from titles, genre, platform where titles.genre = genre.id and titles.platform = platform.id "
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("viewTitles.html", the_data = data)

#creates a new review and inserts variables into database
def createReview(game_id,user_id,liked,played,owned,rating,comment):
    with DBcm.UseDatabase(config) as cursor:
        SQL = "insert into review (game_id,user_id,liked,played,owned,rating,comment) values (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(SQL,(game_id,user_id,liked,played,owned,rating,comment))

#creates a new game and inserts into database
def createGame(name,release_year,studio,genre,platform):
    with DBcm.UseDatabase(config) as cursor:
        SQL = "insert into titles (name,likes,dislikes,release_year,game_studio,genre,platform) values (%s,0,0,%s,%s,%s,%s)"
        cursor.execute(SQL,(name,release_year,studio,genre,platform))

app.secret_key = "Kevin Andersen123 fffffff ggggggg bbbbb"

if __name__ == "__main__":
    app.run(debug=True) 
