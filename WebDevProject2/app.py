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
    return render_template("login.html")

@app.route("/titles", methods=["POST"]) 
def titles():
    with DBcm.UseDatabase(config) as cursor: 
        SQL = """select titles.name, count(titles.likes), count(titles.dislikes), count(titles.comment), titles.release_year, genre.name, titles.game_studio, platform.name from titles, genre, platform where
        titles.genre = genre.id and titles.platform = platform.id"""
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("viewTitles.html", the_data = data)

@app.route("/writeReview")
def writeReview():
    return render_template("writeReview.html")

@app.route("/submitReview", methods=["POST"])
def submitReview():
    with DBcm.UseDatabase(config) as cursor:
        SQL = "update titles set likes = (select count(*) from comment where comment.title_id = 1 && comment.like_dislike = 1) where id =" + session["gameid"]
        cursor.execute(SQL)

    with DBcm.UseDatabase(config) as cursor:
        SQL = "update titles set dislikes = (select count(*) from comment where comment.title_id = 1 && comment.like_dislike = 2 ) where id =" + session["gameid"]
        cursor.execute(SQL)

    with DBcm.UseDatabase(config) as cursor:
        SQL = "update titles set no_comments = (select count(*) from comment where comment.title_id = " + session["gameid"]+ ") where id =" + session["gameid"]
        cursor.execute(SQL)

    with DBcm.UseDatabase(config) as cursor:
        SQL = """select titles.id, titles.name , titles.likes , titles.dislikes , titles.no_comments , titles.release_year , genre.name , titles.game_studio , platform.name from titles,genre,platform  
                 where titles.genre = genre.id and titles.platform = platform.id"""
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("viewTItles.html", the_data = data)

@app.route("/gameDetails", methods=["POST"])
def gameDetails():
    session["gameID"] = request.form["gameID"]
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select * from comment where comment.title_id = " + session["gameID"]
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("gameDetails.html", the_data = data)

@app.route("/insertGamePage")
def insertGamePage():
     with DBcm.UseDatabase(config) as cursor:
        SQL = "select * from genre"
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("newGame.html", the_data = data)

@app.route("/insertNewGame" , methods=["POST"])
def insertNewGame():
     with DBcm.UseDatabase(config) as cursor:
        SQL = """select titles.id, titles.name , titles.likes , titles.dislikes , titles.no_comments , titles.release_year , genre.name , titles.game_studio , platform.name from titles,genre,platform  
                 where titles.genre = genre.id and titles.platform = platform.id"""
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("viewTitles.html", the_data = data)
    
app.secret_key = "Kevin Andersen123 fffffff ggggggg bbbbb"

if __name__ == "__main__":
    app.run(debug=True) 
