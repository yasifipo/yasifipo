from flask import Blueprint
from flask_login import login_required, login_user, logout_user
from app import bcrypt

admin = Blueprint('admin', __name__, template_folder='templates')

from modules.site import *
from modules.page import *
from modules.tag import *
from modules.prez import *
from modules.post import *
from modules.menu import *
from modules.plugin import *
from modules.api import *
from modules.rule import *
from modules.collection import *

from .user import *

@admin.route('/')
@login_required
def admin_root():
	return render_template('admin/admin.html')

@admin.route('/reloading', methods=['POST'])
@login_required
def reloading():

	app.maintenance = True

	app.yasifipo = {}
	app.yasifipo['config'] = {} #config
	app.yasifipo['toc'] = {} # toc for prez
	app.yasifipo['ids'] = {} # rule --> file
	app.yasifipo['root'] = {} # website root info
	app.yasifipo['files'] = {} # file --> rule
	app.yasifipo['langs'] = {} # langs data
	app.yasifipo['refs'] = {} # refs used for retrieve all langs of an object
	app.yasifipo['tags'] = {}
	app.yasifipo['i18n'] = {}
	app.yasifipo['posts'] = {}
	app.yasifipo['collections'] = {} #collections
	app.yasifipo['prezs'] = {}
	app.yasifipo["sitedata"] = None
	app.yasifipo["menu"] = {} #menus
	app.plugins = {}

	init_api()
	init_plugins()
	init_file_data()
	init_i18n_data()
	init_lang_data()
	init_tag_data()
	#No init_site_data --> path already registered
	init_rules()
	init_prez_data()
	init_page_data()
	init_post_data()
	init_collection_data()
	init_menu_data()

	app.maintenance = False

	return redirect(url_for('admin.admin_root'))

@admin.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('admin/login.html')

	password = request.form['password']

	user = None
	if bcrypt.check_password_hash(get_password_hash(), password):
		user = User()

	if user is None:
		return redirect(url_for('admin.login'))

	login_user(user)
	return redirect(request.args.get('next') or url_for('render_root'))

@admin.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('render_root'))
