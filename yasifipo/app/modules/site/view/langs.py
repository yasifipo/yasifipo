from app import app

from os.path import isfile, isdir
from os import listdir
from frontmatter import load


from .urls import *
import modules.site
from modules.utils.util_yaml import *

def init_lang_data():

	listfile = listdir(app.config["LANGS_DIR"])
	for lang in listfile:
		if isfile(app.config["LANGS_DIR"] + lang):
			if app.spec.match_file(lang):
				continue
			with open(app.config["LANGS_DIR"] + lang, encoding='utf-8') as fil_:
				lang_ = load(fil_)
				app.yasifipo['langs'][lang_['lang']] = {'lang':lang_['lang'], 'descr': lang_['descr'], 'sort':int(lang_['sort'])}
				if not 'draft' in lang_.keys() or ('draft' in lang_.keys() and lang_['draft'] == False):
					app.yasifipo['langs'][lang_['lang']]['draft'] = False
				else:
					app.yasifipo['langs'][lang_['lang']]['draft'] = True

def set_lang(yaml):
	lang = ''
	# if no lang in file, set to default lang
	if 'lang' not in yaml.keys():
		lang = app.yasifipo["config"]["default_lang"]
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
		fil_.write('draft: True' + '\n')
		fil_.write('---\n')
		fil_.close()
		print("New language detected : " + lang)
		app.yasifipo['langs'][lang] = {'lang':lang, 'descr': lang, 'sort':99, 'draft': True}

    	# update files needed

		# Update i18n files
		listfile = listdir(app.config["I18N_DIR"])
		for file_ in listfile:
			if isfile(app.config["I18N_DIR"] + "/" + file_):
				if app.spec.match_file(file_):
					continue
				with open(app.config["I18N_DIR"] + "/" + file_, encoding='utf-8') as fil_data:
					yaml = load(fil_data)
					for slug in yaml['labels'].keys():
						yaml['labels'][slug][lang] = app.yasifipo["i18n"][yaml['slug']][slug][app.yasifipo["config"]["default_lang"]]
				fil_write = open(app.config["I18N_DIR"] + "/" + file_, "w", encoding='utf-8')
				fil_write.write(yaml_dump(yaml))
				fil_write.close()

		# Update tags summary
		with open(app.config["TAG_DIR"] + "/summary.md", encoding='utf-8') as fil_data:
			yaml = load(fil_data)
			for tag in yaml['tags']:
				tag['descr'][lang] = app.yasifipo["tags"]["conf"][tag['slug']]['descr'][app.yasifipo["config"]["default_lang"]]
				tag['url']['mass'][lang] = lang + "/" + tag['slug']
				tag['url']['url'][lang] = lang + "/" + tag['slug']

			fil_write = open(app.config["TAG_DIR"] + "/summary.md", "w", encoding='utf-8')
			fil_write.write(yaml_dump(yaml))
			fil_write.close()

			for tag in yaml['tags']:
				if not isdir(app.config['TAG_DIR'] + "/" + tag['directory']):
					continue

				files = listdir(app.config['TAG_DIR'] + "/" + tag['directory'])
				for file_ in files:
					if app.spec.match_file(file_):
						continue
					with open(app.config['TAG_DIR'] + "/" + tag['directory'] + "/" + file_, encoding='utf-8') as fil_tag:
						yaml = load(fil_tag)
						yaml['descr'][lang] = app.yasifipo["tags"]["data"][tag['slug']][yaml['slug']]['descr'][app.yasifipo["config"]["default_lang"]]
						yaml['url'][lang] = lang + "/" + yaml['slug']

						fil_write = open(app.config['TAG_DIR'] + "/" + tag['directory'] + "/" + file_, "w", encoding='utf-8')
						fil_write.write(yaml_dump(yaml))
						fil_write.close()

		# Update collection descriptions
		with open(app.config["COLLECTION_DIR"] + "/summary.md", encoding='utf-8') as fil_data:
			yaml = load(fil_data)
			for coll in yaml['collections']:
				coll['description'][lang] = coll['description'][app.yasifipo["config"]["default_lang"]]

			fil_write = open(app.config["COLLECTION_DIR"] + "/summary.md", "w", encoding='utf-8')
			fil_write.write(yaml_dump(yaml))
			fil_write.close()

	return lang

def get_langs_from_ref(ref_):
	langs = []
	if 'ref' in ref_.keys():
		ref = ref_['ref']
		for lang in app.yasifipo["refs"][ref].values():
			if app.yasifipo["langs"][lang['lang']]["draft"] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue
			langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('render_file', path=app.yasifipo["files"][app.yasifipo["refs"][ref][lang['lang']]['file']])})
	return sorted(langs, key=lambda k: k['sort'])

def get_langs_from_tag(tag_type, tag):
	langs = []
	for lang in app.yasifipo['langs'].values():
		if app.yasifipo["langs"][lang['lang']]["draft"] == True:
			if app.config['DISPLAY_ALL'] == False:
				continue
		if len(app.yasifipo["tags"]["data"][tag_type][tag]['data'][lang['lang']]) == 0:
			continue
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('render_file', path=app.yasifipo["tags"]["data"][tag_type][tag]['url'][lang['lang']])})
	return sorted(langs, key=lambda k: k['sort'])

def get_langs_from_tag_type(tag_type):
	langs = []
	for lang in app.yasifipo['langs'].values():
		if app.yasifipo["langs"][lang['lang']]["draft"] == True:
			if app.config['DISPLAY_ALL'] == False:
				continue

		data_found = False
		for tag in app.yasifipo["tags"]["data"][tag_type].keys():
			if len(get_langs_from_tag(tag_type, tag)) >= 2:
				data_found = True
				break
		if data_found == False:
			continue
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('render_file', path=app.yasifipo["tags"]["conf"][tag_type]['urls']['mass'][lang['lang']])})
	return sorted(langs, key=lambda k: k['sort'])
