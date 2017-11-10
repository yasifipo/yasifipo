import os
from app import manager
from main import app
from flask_frozen import Freezer
from flask_script import Option

from modules.site import *
from modules.prez import *
from modules.page import *

freezer = Freezer(app)

@freezer.register_generator
def url_generator():
	for i in app.yasifipo['frozen']:
		yield i[0], i[1]

@manager.command
def freeze(data_path=None):

	option_list = (
        Option('--data', '-d', dest='data_path', required=False),
		)

	if data_path:
		app.config['DATA_DIR'] = os.path.abspath(data_path) + "/"

	load_config()
	run_data_read()
	freezer.freeze()

@manager.command
def run(data_path=None):

	option_list = (
        Option('--data', '-d', dest='data_path', required=False),
		)

	if data_path:
		app.config['DATA_DIR'] = os.path.abspath(data_path) + "/"

	load_config()
	run_data_read()
	app.run()

def run_data_read():
	init_url_data()
	init_prez_data()
	init_pages_data()
	init_categories_data()

if __name__ == '__main__':
	manager.run()
