#!/usr/bin/env python3
import toml
from flask import Flask
from requests import get
from dotenv import load_dotenv

from modules import freebusy, time, weather
import credentials

load_dotenv()

module_classes = {
    "freebusy": freebusy,
    "time": time,
    "weather": weather
}

modules = []

app = Flask(__name__)

@app.before_first_request
def setup_modules():
    # read config
    config = {}
    with open('/inkydash/config/inkydash.toml', 'r') as file:
        data = file.read()
        config = toml.loads(data)

    # load modules
    for module in config["modules"]:
        imported_module = module_classes[module]
        module_config = config[module] if module in config.keys() else {}
        modules.append(imported_module.module(module_config))
        app.logger.info("loaded module %s", module)

@app.route("/data")
def get_data():
    return list(map(lambda module_instance : module_instance.render(), modules))

