from modules.site import *
from modules.prez import *
from modules.tag import *
from modules.page import *
from modules.init import *
from modules.post import *
from modules.collection import *
from modules.admin import admin
from modules.request_post.views import *
from modules.menu import *
from modules.plugin import *
from modules.api import *
from modules.rule import *

def run_data_read(app):
	app.maintenance = False
	init_api()
	init_plugins()
	init_file_data()
	init_i18n_data()
	init_lang_data()
	init_tag_data()
	init_site_data()
	init_rules()
	init_prez_data()
	init_page_data()
	init_post_data()
	init_collection_data()
	init_menu_data()
	setattr(app.post, "default_post", default_post) # default post result
