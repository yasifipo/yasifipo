from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates')

from modules.site import *
from modules.page import *
from modules.tag import *
from modules.prez import *
from modules.post import *

@admin.route('/')
#TODO login required
def admin_root():
	return render_template('admin/admin.html')

@admin.route('/reloading', methods=['POST'])
#TODO login required
def reloading():

	app.maintenance = True

	app.yasifipo = {}
	app.yasifipo['toc'] = {} # toc for prez
	app.yasifipo['ids'] = {} # rule --> file
	app.yasifipo['root'] = {} # website root info
	app.yasifipo['files'] = {} # file --> rule
	app.yasifipo['langs'] = {} # langs data
	app.yasifipo['refs'] = {} # refs used for retrieve all langs of an object
	app.yasifipo['tags'] = {}
	app.yasifipo['i18n'] = {}

	init_file_data()
	init_i18n_data()
	init_lang_data()
	init_tag_data()
	#No init_site_data --> path already registered
	init_prez_data()
	init_page_data()
	init_post_data()

	app.maintenance = False

	return redirect(url_for('admin.admin_root'))
