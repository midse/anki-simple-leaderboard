from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route("/teams", methods=["GET", "POST"])
def teams():
    if request.method == "POST":
        return ""


@app.route("/teams/<uuid:team_id>", methods=["GET", "PUT"])
def team(username):
    return ""


@app.route("/users", methods=["GET", "POST"])
def users():
    # id : uuid
    # name
    # daily_reviews
    # minutes_reviews
    # streak
    # monthly_reviews
    # retention
    # total_cards

    if request.method == "POST":
        return ""


@app.route("/users/<uuid:user_id>", methods=["GET", "PUT"])
def user(username):
    return ""
