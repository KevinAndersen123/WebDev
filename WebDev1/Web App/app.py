from flask import Flask, render_template, session, request
import random
import pickle
import os

app = Flask(__name__)
FNAME = "data/scores.pickle"

@app.route("/displayscore")
def display_score():
    score = random.randint(0, 100)
    session["score"] = score
    return render_template("score.html", 
        the_score=score,
        the_title="Here is your High Score",)

@app.route("/recordhighscore", methods=["POST"])
def store_score():
    score = session["score"]
    player_name = request.form["player"]
    #if file doesnt exist-create a new empty pickle file
    #if the file does exist-grab the current data stored in the pickle.

    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
    data.append((score, player_name))
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)
    return "Your highscore has been recorded"

@app.route("/showhighscores")
def show_scores():
    with open(FNAME, "rb") as pf:
            data = pickle.load(pf)

    return render_template("winners.html",the_title = "Here are the highscores", the_data = sorted(data,reverse=True),)
app.secret_key = "flkgdn kldndfngfjdngrnfjngfjgb yrbbebisbfidbb "
app.run(debug=True)