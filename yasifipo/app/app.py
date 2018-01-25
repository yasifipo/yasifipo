from flask import Flask
from flask_script import Manager
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Configuration
from flask_frozen import Freezer

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

freezer = Freezer(app)

app.yasifipo = {}
app.yasifipo['config'] = {} #config
app.yasifipo['toc'] = {} # toc for prez
app.yasifipo['ids'] = {} # rule --> file
app.yasifipo['root'] = {} # website root info
app.yasifipo['files'] = {} # file --> rule
app.yasifipo['langs'] = {} # langs data
app.yasifipo['refs'] = {} # refs used for retrieve all langs of an object
app.yasifipo['tags'] = {} #tags
app.yasifipo['i18n'] = {} #translation
app.yasifipo['posts'] = {} #posts
app.yasifipo['collections'] = {} #collections
app.yasifipo['prezs'] = {}
app.yasifipo["sitedata"] = None
app.yasifipo["menu"] = {} #menus
app.plugins = {}
