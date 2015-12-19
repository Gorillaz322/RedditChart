from flask import Flask
from main import config

app = Flask(__name__, static_url_path='/static')
app.debug = config.DEBUG

import main.views
