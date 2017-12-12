import os
from app import manager
from main import app
from flask_frozen import Freezer
from flask_script import Option

from modules.site import *
from modules.prez import *
from modules.tag import *
from modules.page import *

freezer = Freezer(app)

@freezer.register_generator
def url_generator():
	for i in app.yasifipo['ids'].keys():
		if app.yasifipo['ids'][i]['type'] == 'img':
			yield 'return_file', {'id_': i}
		else:
			yield 'render_file', {'path': i}

@manager.option('-d', '--data', dest='data_path', default=None)
@manager.option('-a', '--all', dest='display_all', default=False)
def freeze(data_path, display_all):

	if data_path:
		app.config['DATA_DIR'] = os.path.abspath(data_path) + "/"

	if display_all:
		app.config['DISPLAY_ALL'] = True
	else:
		app.config['DISPLAY_ALL'] = False

	load_config()
	run_data_read()
	freezer.freeze()

@manager.option('-d', '--data', dest='data_path', default=None)
@manager.option('-a', '--all', dest='display_all', default=False)
def run(data_path, display_all):

	if data_path:
		app.config['DATA_DIR'] = os.path.abspath(data_path) + "/"

	if display_all:
		app.config['DISPLAY_ALL'] = True
	else:
		app.config['DISPLAY_ALL'] = False

	load_config()
	run_data_read()
	app.run()

def run_data_read():
	init_file_data()
	init_i18n_data()
	init_lang_data()
	init_tag_data()
	init_site_data()
	init_prez_data()
	init_page_data()

if __name__ == '__main__':
	manager.run()
