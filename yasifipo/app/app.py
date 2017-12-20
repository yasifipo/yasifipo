from flask import Flask
from flask_script import Manager
from config import Configuration

# static rule will be generated later
app = Flask(__name__, static_url_path=None, static_folder=None)
app.config.from_object(Configuration)

manager = Manager(app)
