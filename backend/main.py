from flask import Flask, url_for, abort, jsonify, request, render_template
from markupsafe import escape
import redis
import datetime
import json
import uuid


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


def stat_key(user_id):
    return f"stat::{user_id}"


def owners_key():
    return "owners"


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


@app.route("/teams/", methods=["GET", "POST"])
def teams():
    if request.method == "POST":
        user_id = request.form["user_id"]
        user = r.get(user_key(user_id))

        if not user or r.sismember(owners_key(), user_id):
            abort(400)

        team_id = str(uuid.uuid4())
        team_details = {
            "owner": user_id,
            "team_id": team_id,
            "team_name": request.form["team_name"],
            "team_desc": request.form["team_desc"],
        }

        # Set up team details
        r.set(team_key(team_id, details=True), json.dumps(team_details))

        # Owner must be part of its own team
        r.sadd(team_key(team_id), request.form["user_id"])

        # Add user to owner list to avoid multiple teams for one user
        r.sadd(owners_key(), user_id)

        return jsonify(team_details)

    if request.method == "GET":
        if user_id := request.args.get("user_id"):
            if not r.get(user_key(user_id)):
                abort(404)

            return render_template("create_team.html", user_id=user_id)
        else:
            teams = []

            for key in r.keys("team::*::details"):
                teams.append(json.loads(r.get(key)))
            return jsonify(teams)


@app.route("/teams/<uuid:team_id>", methods=["GET", "PUT"])
def team(team_id):
    team = r.get(team_key(team_id, details=True))

    if not team:
        abort(404)

    if request.method == "PUT":
        abort(400)

    return jsonify(json.loads(team))


@app.route("/users/", methods=["GET", "POST"])
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

    user = json.loads(user)
    user["stats"] = {}

    stats = r.hgetall(stat_key(user_id))

    for key, value in stats.items():
        user["stats"][str(key, "utf8")] = json.loads(value)

    return jsonify(user)


@app.route("/stats/", methods=["POST"])
def stats():
    # user_id : uuid
    # daily_reviews
    # minutes_reviews
    # streak
    # monthly_reviews
    # retention
    # total_cards
    if request.method == "POST":
        user_id = request.form["user_id"]

        user = r.get(user_key(user_id))

        if not user:
            abort(400)

        stats = {
            "streak": request.form["streak"],
            "total_cards": request.form["total_cards"],
            "time_today": request.form["time_today"],
            "past_30_days": request.form["past_30_days"],
            "retention": request.form["retention"],
        }
        r.hset(
            stat_key(user_id),
            datetime.date.today().strftime("%Y%m%d"),
            json.dumps(stats),
        )

        return jsonify(stats)
