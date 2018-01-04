import os
from app import manager
from app import bcrypt
from app import app
from main import app
from flask_frozen import Freezer
from flask_script import Option

from modules.site import *
from modules.prez import *
from modules.tag import *
from modules.page import *
from modules.init import *
from modules.post import *
from modules.collection import *
from modules.admin import admin
from modules.request_post.views import *

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

	if 'dont_freeze' in app.yasifipo['config'] and app.yasifipo['config']['dont_freeze'] == True:
		print("Can't freeze. Check config")
		return

	templates_loader()

	if 'yasifipo_subdirectory' in app.yasifipo['config'] and app.yasifipo['config']['yasifipo_subdirectory'] != '':
		app.config['FREEZER_DESTINATION'] = app.config['FREEZER_DESTINATION'] + "/" + app.yasifipo['config']['yasifipo_subdirectory']

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
	templates_loader()

	if 'yasifipo_subdirectory' in app.yasifipo['config'] and app.yasifipo['config']['yasifipo_subdirectory'] != '':
		app.register_blueprint(admin, url_prefix="/" + app.yasifipo['config']['yasifipo_subdirectory'] + "/admin")
	else:
		app.register_blueprint(admin, url_prefix="/admin")

	app.run()

@manager.option('-d', '--data', dest='data_path', required=True)
def init(data_path):

	if isdir(os.path.abspath(data_path)):
		print('Path already exists ... Exiting wihout initialisation')
		return

	init_yasifipo_minimal(os.path.abspath(data_path))

@manager.option('-d', '--data', dest='data_path', required=True)
def example(data_path):

	if isdir(os.path.abspath(data_path)):
		print('Path already exists ... Exiting wihout example copy')
		return

	init_yasifipo_example(os.path.abspath(data_path))

@manager.option('-p', '--password', dest='password', required=True)
def admin_password(password):

	if(password):
		file_ = open('app/pass.md', 'w')
		file_.write('---\n')
		file_.write('pass: ' + bcrypt.generate_password_hash(password).decode('utf-8')  + "\n")
		file_.write('---\n')
		file_.close()


def run_data_read():
	app.maintenance = False
	init_file_data()
	init_i18n_data()
	init_lang_data()
	init_tag_data()
	init_site_data()
	init_prez_data()
	init_page_data()
	init_post_data()
	init_collection_data()
	setattr(app.post, "default_post", default_post) # default post result

if __name__ == '__main__':
	manager.run()
