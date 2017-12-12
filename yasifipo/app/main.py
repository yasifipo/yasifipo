from app import app

from frontmatter import load

from flask_frozen import Freezer

from modules.admin import admin

freezer = Freezer(app)

app.yasifipo = {}
app.yasifipo['toc'] = {} # toc for prez
app.yasifipo['ids'] = {} # rule --> file
app.yasifipo['root'] = {} # website root info
app.yasifipo['files'] = {} # file --> rule
app.yasifipo['langs'] = {} # langs data
app.yasifipo['refs'] = {} # refs used for retrieve all langs of an object
app.yasifipo['tags'] = {}
app.yasifipo['i18n'] = {}

app.register_blueprint(admin, url_prefix="/admin")
