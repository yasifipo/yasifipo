from app import app

from os.path import isfile, isdir
from os import listdir
from frontmatter import load, dumps

from .urls import *
import modules.site

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

    	# update files needed

		# Update i18n files
		listfile = listdir(app.config["I18N_DIR"])
		for file_ in listfile:
			if isfile(app.config["I18N_DIR"] + "/" + file_):
				with open(app.config["I18N_DIR"] + "/" + file_) as fil_data:
					yaml = load(fil_data)
					for slug in yaml['labels'].keys():
						app.yasifipo["i18n"][yaml['slug']][slug][lang] = app.yasifipo["i18n"][yaml['slug']][slug][app.config["DEFAULT_LANG"]]
						yaml['labels'][slug][lang] = app.yasifipo["i18n"][yaml['slug']][slug][app.config["DEFAULT_LANG"]]
				fil_write = open(app.config["I18N_DIR"] + "/" + file_, "w")
				fil_write.write(dumps(yaml))
				fil_write.close()

		# Update tags summary
		with open(app.config["TAG_DIR"] + "/summary.md") as fil_data:
			yaml = load(fil_data)
			for tag in yaml['tags']:
				app.yasifipo["tags"]["conf"][tag['slug']]['descr'][lang] = app.yasifipo["tags"]["conf"][tag['slug']]['descr'][app.config["DEFAULT_LANG"]]
				tag['descr'][lang] = app.yasifipo["tags"]["conf"][tag['slug']]['descr'][app.config["DEFAULT_LANG"]]

				app.yasifipo["tags"]["conf"][tag['slug']]['urls']['mass'][lang] = lang + "/" + tag['slug']
				tag['url']['mass'][lang] = lang + "/" + tag['slug']

				app.yasifipo["tags"]["conf"][tag['slug']]['urls']['url'][lang] = lang + "/" + tag['slug']
				tag['url']['url'][lang] = lang + "/" + tag['slug']

			fil_write = open(app.config["TAG_DIR"] + "/summary.md", "w")
			fil_write.write(dumps(yaml))
			fil_write.close()

			for tag in yaml['tags']:
				if not isdir(app.config['TAG_DIR'] + "/" + tag['directory']):
					continue

				files = listdir(app.config['TAG_DIR'] + "/" + tag['directory'])
				for file_ in files:
					with open(app.config['TAG_DIR'] + "/" + tag['directory'] + "/" + file_) as fil_tag:
						yaml = load(fil_tag)
						app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['descr'][lang] = app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['descr'][app.config["DEFAULT_LANG"]]
						yaml['descr'][lang] = app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['descr'][app.config["DEFAULT_LANG"]]

						app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['url'][lang] = app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['url'][app.config['DEFAULT_LANG']]
						yaml['url'][lang] = lang + "/" + yaml['slug']

						app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['data'][lang] = {}

						fil_write = open(app.config['TAG_DIR'] + "/" + tag['directory'] + "/" + file_, "w")
						fil_write.write(dumps(yaml))
						fil_write.close()

		# register new lang when needed
		# register mass urls
		for tag in app.yasifipo["tags"]["conf"].keys():
			rule = app.yasifipo["tags"]["conf"][tag]["urls"]['mass'][lang]
			modules.site.yasifipo_register("tag_type", rule, None, {'tag_type': tag, 'lang':lang})

		for tag_type in app.yasifipo["tags"]["data"].keys():
			for tag in app.yasifipo["tags"]["data"][tag_type].keys():
				rule = app.yasifipo["tags"]["data"][tag_type][tag]['url'][lang]
				modules.site.yasifipo_register("tag", rule, None, {'tag_type': tag_type, 'tag': tag, 'lang': lang })


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
