from app import app
from modules.site import *

def get_category_langs(category):
	langs = []
	for lang in app.yasifipo["categories"][category].values():
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('display_category', category=category, lang=lang['lang'] )})
	return sorted(langs, key=lambda k: k['sort'])
