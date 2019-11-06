from flask import Flask, render_template, session, request
import random
import pickle
import os
import datetime

LEADERBOARD = "data/leaderboard.pickle"
app = Flask(__name__)
@app.route("/guessingGame")
def guessNumber():
    randNum = random.randint(0,1000)
    session["number"] = randNum
    session["guess"] = 0
    return render_template(
        "game.html",
        the_title = "Guess the Number",
        the_number = randNum,
        the_script = "",
        the_num = randNum
    )
@app.route("/guessedNumber", methods =["POST"])
def guessedNumber():
    randNum = session["number"]
    if request.form["guessedNumber"] == "":
        return render_template( 
        "game.html",
        the_title = "Guess the Number",
        the_number = randNum,
        the_script = "Input a number",
        )
    else:
        numberGuessed = (int)(request.form["guessedNumber"])

        session["guess"] = session["guess"] + 1
        noOfGuesses = session["guess"]
    if numberGuessed > randNum:
        return render_template( 
        "game.html",
        the_title = "Guess the Number",
        the_number = randNum,
        the_script = "Your guess is too high"
        )
    elif numberGuessed < randNum:
        return render_template( 
        "game.html",
        the_title = "Guess the Number",
        the_number = randNum,
        the_script = "Your guess is too low"
        )
    else :
        return render_template( 
        "score.html",
        the_title = "Guess the Number",
        the_number = randNum,
        the_guesses = noOfGuesses
        )
@app.route("/recordName", methods =["POST"])
def storeScore():
    player_name = request.form["player_name"]
    player_guess = session["guess"]
    if not os.path.exists(LEADERBOARD):
        data = []
    else: 
        with open(LEADERBOARD,"rb") as pf:
            data = pickle.load(pf)
    data.append((player_guess,player_name))
    with open(LEADERBOARD,"wb") as pf:
            pickle.dump(data,pf)
    return "Your name and score is now recorded"
@app.route("/highscore")
def show_highscores():
       with open(LEADERBOARD,"rb") as pf:
            data = pickle.load(pf)
       return render_template(
            "leaderboard.html",
            the_title = "Highscores",
            the_data = data
        )
    
app.secret_key = "Kevin123 ggwp"

app.run(debug=True)