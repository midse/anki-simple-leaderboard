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

from aqt import mw, gui_hooks
from aqt.qt import QMenu
from aqt.utils import showText
from .stats import stats
from .utils import logger, create_or_update_user, update_stats


def hook_profile_open():
    logger.info("Profile open!")

    results = stats()
    logger.info(results)
    update_stats(results)


def hook_profile_close():
    logger.info("Profile close!")

    if not create_or_update_user():
        logger.critical("Unable to update user information!")
        return

    results = stats()
    logger.info(results)
    update_stats(results)

def display_leaderboard():
    txt = "HEY"
    showText(
    txt,
    type="html",
    title="Leaderboard",
)


logger.info("Launching leaderboard...")

if not create_or_update_user():
    logger.critical("Unable to update user information!")
else:
    # Linking hooks
    gui_hooks.profile_did_open.append(hook_profile_open)
    gui_hooks.profile_will_close.append(hook_profile_close)

    pa_menu = QMenu('Leaderboard', mw)
    pa_menu_display = pa_menu.addAction('Display')
    pa_menu_create = pa_menu.addAction('Create team')
    # # add triggers
    pa_menu_display.triggered.connect(display_leaderboard)
    # pa_menu_remove.triggered.connect(remove_pitch_dialog)
    # and add it to the tools menu
    mw.form.menuTools.addMenu(pa_menu)
