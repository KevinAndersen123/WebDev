from flask import Flask, render_template, session, request
import random
import pickle
import os

app = Flask(__name__)
FNAME = "data/randNumber.pickle"
randomNumber = random.randint(0, 1000)
@app.route("/guessingGame")
def game():
    return render_template("game.html", 
    the_title="Guess the Number")

@app.route("/response", methods = ["POST"])
def response():
    guess_number = request.form["number"]
    response = ""
    if(guess_number == randomNumber):
        response = "Congratulations, you guessed correctly!"
    elif(guess_number < randomNumber):
           response = "Sorry, your guess is too low"
    else:
        response = "Sorry, your guess is too high"
@app.route("/storeGuessedNum", methods=["POST"])
def store_number():
    guessed_num = request.form["number"]
    #if file doesnt exist-create a new empty pickle file
    #if the file does exist-grab the current data stored in the pickle.
    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
            data.append(randomNumber,guessed_num)
    with open(FNAME, "wb") as pf:
         pickle.dump(data, pf)
    return 
app.secret_key = "flkgdn kldndfngfjdngrnfjngfjgb yrbbebisbfidbb "
app.run(debug=True)