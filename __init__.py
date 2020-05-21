# Copyright 2020 Dimitri Ségard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import uuid
import os
import logging
import requests

from aqt import mw, gui_hooks
from .stats import stats
from .utils import logger


def profile_open():
    logger.info("Profile open!")
    logger.info(stats())


def profile_close():
    logger.info("Profile close!")
    logger.info(stats())


logger.info("Launching leaderboard...")

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
    logger.info(r.json())
    gui_hooks.profile_did_open.append(profile_open)
    gui_hooks.profile_will_close.append(profile_close)
except:
    logger.critical("Unable to update user information!")
