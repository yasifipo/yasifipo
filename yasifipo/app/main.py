from app import app

from frontmatter import load

from flask_frozen import Freezer

from modules.prez import *
from modules.page import *
from modules.site import *

freezer = Freezer(app)

app.yasifipo = {}
app.yasifipo['toc'] = {}
app.yasifipo['frozen'] = []
app.yasifipo['langs'] = {}
app.yasifipo["refs"] = {}
app.yasifipo["categories"] = {}
app.yasifipo["cat_ref"] = {}
app.yasifipo["urls"] = {}

init_url_data()
init_prez_data()
init_pages_data()
init_categories_data()
