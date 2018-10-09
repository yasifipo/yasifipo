import os
from app import manager
from app import bcrypt
from app import app
from flask_frozen import Freezer
from flask_script import Option

from main import *
from modules.site import *

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
@manager.option('-s', '--server', dest='runtime_server', default=None)
def freeze(data_path, display_all, runtime_server):

	if data_path:
		app.config['DATA_DIR'] = os.path.abspath(data_path) + "/"

	if display_all:
		app.config['DISPLAY_ALL'] = True
	else:
		app.config['DISPLAY_ALL'] = False

	# change build directory based on data dir
	app.config['FREEZER_DESTINATION'] = app.config['DATA_DIR'] + app.config['FREEZER_DESTINATION']

	load_config()

	if runtime_server:
		app.config['RUNTIME_SERVER'] = runtime_server
	else:
		app.config['RUNTIME_SERVER'] = None

	run_data_read(app)
	templates_add_loader(app.config['APPLICATION_DIR'] + "/" + "templates/" + app.config["APPLICATION_TEMPLATE"] + "/", init=True)
	templates_add_loader(app.config['TEMPLATES_DIR'] + app.yasifipo["config"]["theme"]) #must be before Plugin registration

	# override build directory based on data config (no more on app config)
	if 'freeze_dir' in app.yasifipo['config']:
		app.config['FREEZER_DESTINATION'] = app.config['DATA_DIR'] + app.yasifipo['config']['freeze_dir']

	# manage not deleted files/dir in build directory, based on data config
	if 'freeze_destination_ignore' in app.yasifipo['config']:
		app.config['FREEZER_DESTINATION_IGNORE'] = app.yasifipo['config']['freeze_destination_ignore']

	if 'dont_freeze' in app.yasifipo['config'] and app.yasifipo['config']['dont_freeze'] == True:
		print("Can't freeze. Check config")
		return

	if 'yasifipo_subdirectory' in app.yasifipo['config'] and app.yasifipo['config']['yasifipo_subdirectory'] != '':
		app.config['FREEZER_DESTINATION'] = app.config['FREEZER_DESTINATION'] + "/" + app.yasifipo['config']['yasifipo_subdirectory']

	freezer.freeze()

@manager.option('-d', '--data', dest='data_path', default=None)
@manager.option('-a', '--all', dest='display_all', default=False)
@manager.option('-s', '--server', dest='runtime_server', default=None)
def run(data_path, display_all, runtime_server):

	if data_path:
		app.config['DATA_DIR'] = os.path.abspath(data_path) + "/"

	if display_all:
		app.config['DISPLAY_ALL'] = True
	else:
		app.config['DISPLAY_ALL'] = False

	load_config()

	if runtime_server:
		app.config['RUNTIME_SERVER'] = runtime_server
	else:
		app.config['RUNTIME_SERVER'] = None

	run_data_read(app)
	templates_add_loader(app.config['APPLICATION_DIR'] + "/" + "templates/"  + app.config["APPLICATION_TEMPLATE"] + "/", init=True)
	templates_add_loader(app.config['TEMPLATES_DIR'] + app.yasifipo["config"]["theme"]) #must be before Plugin registration

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
