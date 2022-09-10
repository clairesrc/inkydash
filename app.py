#!/usr/bin/env python3
import os
from flask import Flask
from dotenv import load_dotenv

from inkydash import InkyDash

load_dotenv()
id = InkyDash()
app = Flask(__name__)


@app.before_first_request
def setup_app():
    id.setup(InkyDash.get_config("/inkydash/config/inkydash.toml"), os.environ)


@app.route("/data")
def get_data():
    return id.render()

