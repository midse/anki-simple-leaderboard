from flask import Flask, url_for, abort, jsonify, request
from markupsafe import escape
import redis
import json

app = Flask(__name__)
pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
r = redis.Redis(connection_pool=pool)


def team_key(team_id, details=False):
    key = f"team::{team_id}"

    if details:
        key += "::details"

    return key


def user_key(user_id):
    return f"user::{user_id}"


def create_or_update_user(form):
    user_id = form["user_id"]
    user_name = form["user_name"]
    team_id = form["team_id"]

    user_data = {
        "user_id": user_id,
        "user_name": user_name,
        "team_id": team_id,
    }
    user = r.get(user_key(user_id))

    if user:
        user = json.loads(user)

        # Updating team
        if team_id != user["team_id"]:
            r.srem(team_key(user["team_id"]), user_id)
            r.sadd(team_key(team_id), user_id)

    r.set(user_key(user_id), json.dumps(user_data))

    return user_data


@app.route("/teams", methods=["GET", "POST"])
def teams():
    if request.method == "POST":
        team_id = request.form["team_id"]
        user_id = request.form["user_id"]

        if r.get(team_key(team_id, details=True)) or not r.get(user_key(user_id)):
            abort(400)

        team_details = {
            "owner": user_id,
            "team_id": team_id,
            "team_name": request.form["team_name"],
            "team_desc": request.form["team_desc"],
        }
        r.set(team_key(team_id, details=True), json.dumps(team_details))
        r.sadd(team_key(team_id), request.form["user_id"])

        return jsonify(team_details)

    teams = []

    for key in r.keys("team::*::details"):
        teams.append(json.loads(r.get(key)))
    return jsonify(teams)


@app.route("/teams/<uuid:team_id>", methods=["GET", "PUT"])
def team(username):
    return ""


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        return create_or_update_user(request.form)

    users = []

    for key in r.keys("user::*"):
        users.append(json.loads(r.get(key)))
    return jsonify(users)


@app.route("/users/<uuid:user_id>", methods=["GET", "PUT"])
def user(user_id):

    user = r.get(user_key(user_id))

    if not user:
        abort(404)

    if request.method == "PUT":
        return create_or_update_user(request.form)

    return jsonify(json.loads(user))


@app.route("/stats/", methods=["POST"])
def stats():
    # user_id : uuid
    # daily_reviews
    # minutes_reviews
    # streak
    # monthly_reviews
    # retention
    # total_cards
    pass
