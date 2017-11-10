from app import app

from frontmatter import load

from flask_frozen import Freezer

freezer = Freezer(app)

app.yasifipo = {}
app.yasifipo['toc'] = {}
app.yasifipo['frozen'] = []
app.yasifipo['langs'] = {}
app.yasifipo["refs"] = {}
app.yasifipo["categories"] = {}
app.yasifipo["cat_ref"] = {}
app.yasifipo["urls"] = {}
