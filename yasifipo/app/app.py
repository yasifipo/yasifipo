from flask import Flask
from flask_script import Manager
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Configuration

from modules.request_post import PostMethod

# static rule will be generated later
app = Flask(__name__, static_url_path=None, static_folder=None)
app.config.from_object(Configuration)

manager = Manager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'

bcrypt = Bcrypt(app)

app.post = PostMethod()
