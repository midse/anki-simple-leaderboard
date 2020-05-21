import os
import uuid
import logging
import requests
from aqt import mw


def config_logger():
    my_logger = logging.getLogger("simple-leaderboard")
    path = os.path.dirname(os.path.realpath(__file__))
    handler = logging.FileHandler(f"{path}/debug.log")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.setLevel(logging.DEBUG)
    return my_logger

def create_or_update_user():
    config = mw.addonManager.getConfig(__name__)

    if not config.get("user_id"):
        config["user_id"] = str(uuid.uuid4())
        logger.info(f"Generating user id : {config['user_id']}")
        mw.addonManager.writeConfig(__name__, config)


    r = requests.get(config["backend_url"] + f"/users/{config['user_id']}")
    data = {
        "user_id": config["user_id"],
        "user_name": config["user_name"],
        "team_id": config["team_id"],
    }

    method = "post" if r.status_code == 404 else "put"
    endpoint = config["backend_url"] + f"/users"

    if method == "put":
        endpoint += "/" + config["user_id"]

    logger.info("Updating user information...")
    r = getattr(requests, method)(endpoint, data=data)

    try:
        r.raise_for_status()
        logger.info(f"Updated information : {r.json()}")
        return True
    except:
        return False

logger = config_logger()
