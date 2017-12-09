from app import app

from os.path import isfile
from os import listdir
from frontmatter import load, dumps

from . import *
from .urls import *

def init_lang_data():

	listfile = listdir(app.config["LANGS_DIR"])
	for lang in listfile:
		if isfile(app.config["LANGS_DIR"] + lang):
			with open(app.config["LANGS_DIR"] + lang) as fil_:
				lang_ = load(fil_)
				app.yasifipo['langs'][lang_['lang']] = {'lang':lang_['lang'], 'descr': lang_['descr'], 'sort':int(lang_['sort'])}

def set_lang(yaml):
	lang = ''
	# if no lang in file, set to default lang
	if 'lang' not in yaml.keys():
		lang = app.config['DEFAULT_LANG']
	else:
		lang = yaml['lang']

	# check if lang is already loaded
	if lang not in [lg['lang'] for lg in app.yasifipo['langs'].values()]:
		# if not, create file for this lang
		fil_ = open(app.config["LANGS_DIR"] + lang, "w")
		fil_.write('---\n')
		fil_.write('lang: ' + lang + '\n')
		fil_.write('descr: ' + lang + '\n')
		fil_.write('sort: 99' + '\n')
		fil_.write('---\n')
		fil_.close()
		print("New language detected : " + lang)
		app.yasifipo['langs'][lang] = {'lang':lang, 'descr': lang, 'sort':99}

    # TODO update files needed (category, etc...)
	return lang

def get_langs_from_ref(ref_):
	langs = []
	if 'ref' in ref_.keys():
		ref = ref_['ref']
		for lang in app.yasifipo["refs"][ref].values():
			langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('render_file', path=app.yasifipo["files"][app.yasifipo["refs"][ref][lang['lang']]['file']])})
	return sorted(langs, key=lambda k: k['sort'])

def get_langs_from_tag(tag_type, tag):
	langs = []
	for lang in app.yasifipo['langs'].values():
		#TODO only if there is some tags for this lang
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('render_file', path=app.yasifipo["tags"]["data"][tag_type][tag]['url'][lang['lang']])})
	return sorted(langs, key=lambda k: k['sort'])

def get_langs_from_tag_type(tag_type):
	langs = []
	for lang in app.yasifipo['langs'].values():
		#TODO only if there is some tag_type for this lang
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('render_file', path=app.yasifipo["tags"]["conf"][tag_type]['urls']['mass'][lang['lang']])})
	return sorted(langs, key=lambda k: k['sort'])
