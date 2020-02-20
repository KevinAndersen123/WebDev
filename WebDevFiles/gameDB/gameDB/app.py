from flask import Flask, render_template, request, session, redirect, url_for, flash

import random
import time

import data_utils


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("start_game"))


@app.route("/game")
def start_game():
    session["start_time"] = time.perf_counter()
    session["number"] = random.randint(1, 1000)
    session["attempts"] = 0
    return render_template("guess.html", the_title="Please make a guess")

@app.route("/processguess", methods=["POST"])
def process_guess():
    guess = int(request.form["the_guess"])
    session["attempts"] += 1
    if guess < session["number"]:
        # Too low.
        return render_template(
            "almost.html", the_title="Your guess was incorrect", the_msg="low"
        )
    elif guess > session["number"]:
        # Too high.
        return render_template(
            "almost.html", the_title="Your guess was incorrect", the_msg="high"
        )
    else:
        # Winner!
        session["how_long"] = round(time.perf_counter() - session["start_time"], 2)
        return render_template(
            "winner.html",
            the_title="Congratualtions!!!",
            the_attempts=session["attempts"],
            the_time=session["how_long"],
        )


@app.route("/recordname", methods=["POST"])
def update_high_scores_table():
    who = request.form["the_winner"]
    data_utils.add_to_scores(who, session["how_long"], session["attempts"])
    position = (
        data_utils.get_sorted_leaderboard().index(
            (who, session["how_long"], session["attempts"])
        )
        + 1
    )
    flash(
        f"Well done, you placed {position} out of {len(data_utils.get_sorted_leaderboard())} on the leaderboard."
    )
    return redirect(url_for("start_game"))


@app.route("/highscores")
def display_leaderboard():
    data = data_utils.get_sorted_leaderboard()
    return render_template(
        "high.html",
        the_title="This is the leaderboard",
        the_data=data,
        the_len=len(data),
    )


app.secret_key = "fkdslflsdkgdfhg'adfh8 ejre 'fd'ofd bifjbjb bfjbtr"

if __name__ == "__main__":
    app.run(debug=True)  # never ends...
