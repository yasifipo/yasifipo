from app import app
import jinja2

from .views import *
from .objects import *

from os.path import isdir, isfile
from frontmatter import load

import pathspec


def init_site_data():
	register_rules()
	init_site_data_files()

def init_file_data():
	with open(app.config['CONFIG_DIR'] + 'file_ignore.txt', 'r') as fh:
		app.spec = pathspec.PathSpec.from_lines('gitignore', fh)

	with open(app.config['CONFIG_DIR'] + 'config.md', 'r') as file_:
		yaml = load(file_)
		for key in yaml.keys():
			if type(yaml[key]).__name__ != 'list':
				app.yasifipo['config'][key] = yaml[key]
			else:
				app.yasifipo['config'][key] = []
				for it in yaml[key]:
					app.yasifipo['config'][key].append(it)

def register_rules():

	app.add_url_rule(
						rule='/<path:path>/',
						view_func=render_file,
						defaults={},
						methods=['GET']
						)

	app.add_url_rule(
						rule='/',
						view_func=render_root,
						defaults={},
						methods=['GET']
						)

	app.add_url_rule(
						rule='/<path:id_>',
						view_func=return_file,
						defaults={},
						methods=['GET']
						)

def init_i18n_data():
	listfile = listdir(app.config["I18N_DIR"])
	for file_ in listfile:
		if isfile(app.config["I18N_DIR"] + "/" + file_):
			if app.spec.match_file(file_):
				continue
			with open(app.config["I18N_DIR"] + "/" + file_) as fil_data:
				yaml = load(fil_data)

				app.yasifipo["i18n"][yaml['slug']] = {}
				for slug in yaml['labels'].keys():
					app.yasifipo["i18n"][yaml['slug']][slug] = {}
					for lang in yaml['labels'][slug].keys():
						app.yasifipo["i18n"][yaml['slug']][slug][lang] = yaml['labels'][slug][lang]

def init_site_data_files():
	app.yasifipo["sitedata"] = SiteData(app.config["SITEDATE_DIR"])


def yasifipo_register(type_, rule, id_, data={}):

	if rule != "/" and type_ in ["prez-chapter", "prez", "prez-single", "prez-course", "prez-page"]:
		rule = rule[1:-1]
	elif rule != "/" and type_ in ["img"]:
		rule = rule[1:]

	app.yasifipo["ids"][rule] = {}
	app.yasifipo["ids"][rule]['id'] = id_
	app.yasifipo["ids"][rule]['type'] = type_
	app.yasifipo["ids"][rule]['data'] = data

	app.yasifipo["files"][id_] = rule

	# Root management
	if rule == "/":

		app.yasifipo["root"]['id'] = id_
		app.yasifipo["root"]['type'] = type_
		app.yasifipo["root"]['data'] = data

def check_server(yaml):
	if 'server' in yaml.keys():
		if type(yaml['server']).__name__ == 'str':
			if (yaml['server'] != app.yasifipo["config"]["yasifipo_server"]):
				return False
		elif type(yaml['server']).__name__ == 'list':
			if app.yasifipo["config"]["yasifipo_server"] not in yaml['server']:
				return False
		else:
			return False

	return True

def register_static_img(directory, current_url, static_url):
	listfile_static = listdir(directory)
	if current_url == "":
		url =  "/" + static_url
	else:
		url = "/" + current_url + "/" + static_url
	for file_img in listfile_static:
		if app.spec.match_file(file_img):
			continue
		if isfile(directory + "/" + file_img):
			rule_ = url + "/" + file_img
			yasifipo_register('img', rule_, directory + "/" + file_img)
		elif isdir(directory + "/" + file_img):
			register_static_img(directory + "/" + file_img, url[1:], file_img)

def set_ref(yaml, file_, lang_=None):
	if 'ref' in yaml.keys():
		# store ref in order to get all langs of an object
		if yaml["ref"] not in app.yasifipo["refs"].keys():
			app.yasifipo["refs"][yaml["ref"]] = {}
		lang = ''
		if 'lang' not in yaml.keys():
			if lang_ is None:
				lang = app.yasifipo["config"]["default_lang"]
			else:
				lang = lang_
		else:
			lang = yaml['lang']
		app.yasifipo["refs"][yaml["ref"]][lang] = {'lang': lang, 'file':file_}

def load_config():
	app.config['PREZ_DIR']     = app.config['DATA_DIR'] + "prez/"  # / after
	app.config['LANGS_DIR']    = app.config['DATA_DIR'] + "langs/" # / after
	app.config['TAG_DIR']      = app.config['DATA_DIR'] + "tags/" # / after
	app.config['PAGE_DIR']     = app.config['DATA_DIR'] + "page/" # / after
	app.config['I18N_DIR']     = app.config['DATA_DIR'] + "i18n/" # / after
	app.config['CONFIG_DIR']   = app.config['DATA_DIR'] + "config/"  # / after
	app.config['POST_DIR']     = app.config['DATA_DIR'] + "post/"  # / after
	app.config['SITEDATE_DIR'] = app.config['DATA_DIR'] + "site_data/" # / after
	app.config['COLLECTION_DIR'] = app.config['DATA_DIR'] + "collections/" # / after
	app.config['TEMPLATES_DIR'] = app.config['DATA_DIR'] + "templates/" # / after

def templates_loader():
	my_loader = jinja2.ChoiceLoader([
	    jinja2.FileSystemLoader(app.config['TEMPLATES_DIR']),
	    app.jinja_loader,
	])
	app.jinja_loader = my_loader
