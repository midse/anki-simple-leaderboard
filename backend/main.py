from flask import Flask, url_for, abort, jsonify, request
from markupsafe import escape
import redis
import json

app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

def create_or_update_user(form):
    user_id = form["user_id"]
    user_name = form["user_name"]
    team_id = form["team_id"]

    user_data = {
        "user_id": user_id,
        "user_name": user_name,
        "team_id": team_id,
    }
    r.set(f"user::{user_id}", json.dumps(user_data))

    return user_data

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
        return create_or_update_user(request.form)


@app.route("/users/<uuid:user_id>", methods=["GET", "PUT"])
def user(user_id):

    user = r.get(f"user::{user_id}")

    if not user:
        abort(404)

    if request.method == "PUT":
        return create_or_update_user(request.form)
    
    return jsonify(json.loads(user))
