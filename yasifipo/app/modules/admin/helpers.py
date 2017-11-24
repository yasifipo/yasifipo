from app import app

from modules.prez import *
from modules.category import *
from modules.page import *
from modules.site import *


def reloading_data():
    # TODO: factorize with manage.py & main.py
	old = app.yasifipo['frozen']
	app.yasifipo = {}
	app.yasifipo['toc'] = {}
	app.yasifipo['frozen'] = []
	app.yasifipo['langs'] = {}
	app.yasifipo["refs"] = {}
	app.yasifipo["categories"] = {}
	app.yasifipo["cat_ref"] = {}
	app.yasifipo["urls"] = {}

	app.yasifipo['old_frozen'] = old

	init_url_data()
	init_prez_data()
	init_pages_data()
	init_categories_data()

	for url in app.yasifipo['old_frozen']:
		pass #TODO
