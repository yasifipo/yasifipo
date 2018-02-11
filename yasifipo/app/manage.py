import os
from app import manager
from app import bcrypt
from app import app
from flask_frozen import Freezer
from flask import render_template
from flask_script import Option

from main import *
from modules.site import *
from os.path import isdir

freezer = Freezer(app)

def generate_redirection(id, url):
	#TODO for https
	html = render_template('site/redirect.html', link="http://" + app.yasifipo['config']['yasifipo_server'] + "/" + url)

	if not isdir(app.config['FREEZER_DESTINATION'] + "/" + id):
		os.makedirs(app.config['FREEZER_DESTINATION'] + "/" + id)
	fil_ = open(app.config['FREEZER_DESTINATION'] + "/" + id + "/index.html", "w")
	fil_.write(html)
	fil_.close()

@freezer.register_generator
def url_generator():
	for i in app.yasifipo['ids'].keys():
		if app.yasifipo['ids'][i]['type'] == 'img':
			yield 'return_file', {'id_': i}
		elif app.yasifipo['ids'][i]['type'] == "redirect":
			generate_redirection(i, yasifipo_url_for('render_file', path=app.yasifipo['ids'][i]['data']['url']))
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

	# change build directory based on data dir
	app.config['FREEZER_DESTINATION'] = app.config['DATA_DIR'] + app.config['FREEZER_DESTINATION']

	load_config()
	templates_add_loader(app.config['TEMPLATES_DIR']) #must be before Plugin registration
	run_data_read(app)

	# override build directory based on data config (no more on app config)
	if 'freeze_dir' in app.yasifipo['config']:
		app.config['FREEZER_DESTINATION'] = app.config['DATA_DIR'] + app.yasifipo['config']['freeze_dir']

	# manage not deleted files/dir in build directory, based on data config
	if 'freeze_destignation_ignore' in app.yasifipo['config']:
		app.config['FREEZER_DESTINATION_IGNORE'] = app.yasifipo['config']['freeze_destignation_ignore']

	if 'dont_freeze' in app.yasifipo['config'] and app.yasifipo['config']['dont_freeze'] == True:
		print("Can't freeze. Check config")
		return

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
	templates_add_loader(app.config['TEMPLATES_DIR']) #must be before Plugin registration
	run_data_read(app)

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

@manager.option('-p', '--password', dest='password', required=True)
def admin_password(password):

	if(password):
		file_ = open('app/pass.md', 'w')
		file_.write('---\n')
		file_.write('pass: ' + bcrypt.generate_password_hash(password).decode('utf-8')  + "\n")
		file_.write('---\n')
		file_.close()


if __name__ == '__main__':
	manager.run()
