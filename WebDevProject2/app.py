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

@app.route("/gameComment")
def writeComment():
    return render_template("writeReview.html")

@app.route("/submitReview", methods=["POST"])
def submitReview():
    with DBcm.UseDatabase(config) as cursor:
        SQL = ""
        cursor.execute(SQL)
        data = cursor.fetchall()
        render_template("viewTitles.html", the_data = data)

@app.route("/gameDetails", methods=["POST"])
def gameDetails():
    session["gameID"] = request.form["gameID"]
    with DBcm.UseDatabase(config) as cursor:
        SQL = "select * from comment where comment.title_id = " + session["gameID"]
        cursor.execute(SQL)
        data = cursor.fetchall()
        return render_template("gameDetails.html", the_data = data)

app.secret_key = "Kevin Andersen123 fffffff ggggggg bbbbb"

if __name__ == "__main__":
    app.run(debug=True) 
