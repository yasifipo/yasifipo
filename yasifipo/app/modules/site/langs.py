from app import app

from os.path import isfile
from frontmatter import load

from . import *

def set_lang(yaml):
	lang = ''
	# if no lang in file, set to default lang
	if 'lang' not in yaml.keys():
		lang = app.config['DEFAULT_LANG']
	else:
		lang = yaml['lang']

	# check if lang is already loaded
	if lang not in [lg['lang'] for lg in app.yasifipo['langs'].values()]:
		# if not, check if file already exists
		if isfile(app.config["LANGS_DIR"] + lang):
			with open(app.config["LANGS_DIR"] + lang) as fil_:
				lang = load(fil_)
				app.yasifipo['langs'][lang['lang']] = {'lang':lang['lang'], 'descr': lang['descr'], 'sort':int(lang['sort'])}
		# if not, create file for this lang
		else:
			# create new lang file
			fil_ = open(app.config["LANGS_DIR"] + lang, "w")
			fil_.write('---\n')
			fil_.write('lang: ' + lang + '\n')
			fil_.write('descr: ' + lang + '\n')
			fil_.write('sort: 99' + '\n')
			fil_.write('---\n')
			fil_.close()
			print("New language detected : " + lang)
			app.yasifipo['langs'][lang] = {'lang':lang, 'descr': lang, 'sort':99}

def get_langs_from_ref(type_, ref, **values):
	langs = []
	for lang in app.yasifipo["refs"][ref].values():
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for(type_, file_=app.yasifipo["refs"][ref][lang['lang']]['file'], lang=lang['lang'], **values)})
	return sorted(langs, key=lambda k: k['sort'])

def new_lang(lang):
	pass
