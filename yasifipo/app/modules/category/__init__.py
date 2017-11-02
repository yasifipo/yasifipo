from frontmatter import load, dumps
from os.path import isfile

from app import app
from .views import *

from slugify import slugify

def init_categories_data():
	# set global url
	with open(app.config["CONFIG_DIR"] + "url") as fil_:
		yaml = load(fil_)
		for lg in yaml['cats'].keys():
			yasifipo_register(yaml['cats'][lg], display_categories, 'display_categories', {'lang': lg})

		# set url for each category
		for cat in app.yasifipo['categories'].values():
			for lg in cat.keys():
				yasifipo_register(yaml['cat'][lg] + cat[lg]['slug'] + '/', display_category, 'display_category', {'category': cat[lg]['cat'], 'lang': lg})

def manage_category(yaml, type_, lang_=None):
	if 'lang' not in yaml.keys():
		if lang_ is None:
			lang = app.config['DEFAULT_LANG']
		else:
			lang = lang_
	else:
		lang = yaml['lang']

	#TODO check there is a ref

	#TODO if a new lang is detected, update config/url.md file

	# Category management
	#TODO default cat if not provided ?
	if 'category' in yaml.keys():
		# check we didn't read the file yet
		if not yaml['category'] in app.yasifipo['categories'].keys():
			# Check if file already exists
			if isfile(app.config["CAT_DIR"] + yaml['category']):
				with open(app.config["CAT_DIR"] + yaml['category']) as fil_:
					cat = load(fil_)
					app.yasifipo['categories'][yaml['category']] = {}
					for lg in cat['descr'].keys():
						app.yasifipo['categories'][yaml['category']][lg] = {'cat': yaml['category'], 'lang': lg,'descr': cat['descr'][lg]['descr'], 'slug': cat['descr'][lg]['slug']}
					# check if lang is known on file
					if lang not in app.yasifipo['categories'][yaml['category']].keys():
						print('New lang ' + lang + ' detected for category ' + yaml['category'])
						cat['descr'][lang] = {'descr': yaml['category'], 'slug':slugify(yaml['category'])}
						#Write category file back with lang
						fil_write = open(app.config["CAT_DIR"] + yaml['category'], "w")
						fil_write.write(dumps(cat))
						fil_write.close()
						app.yasifipo['categories'][yaml['category']][lang] = {'cat': yaml['category'], 'lang': lang,'descr': cat['descr'][lang]['descr'], 'slug': cat['descr'][lang]['slug']}
			else:
				# create new cat file
				fil_ = open(app.config["CAT_DIR"] + yaml['category'], "w")
				fil_.write('---\n')
				fil_.write('category: ' + yaml['category'] + '\n')
				fil_.write('descr:\n')
				fil_.write('  ' + lang +':\n')
				fil_.write('    descr: ' + yaml['category'] + '\n')
				fil_.write('    slug: ' + slugify(yaml['category']) + '\n')
				fil_.write('---\n')
				fil_.close()
				print("New category detected : " + yaml['category'])
				if yaml['category'] not in app.yasifipo['categories'].keys():
					app.yasifipo['categories'][yaml['category']] = {}

				app.yasifipo['categories'][yaml['category']][lang] = {'cat': yaml['category'], 'lang': lang, 'descr': yaml['category'], 'slug': slugify(yaml['category'])}
		else:
			# We already read the file. Check the lang is known
			if lang not in app.yasifipo['categories'][yaml['category']].keys():
				print('New lang ' + lang + ' detected for category ' + yaml['category'])
				with open(app.config["CAT_DIR"] + yaml['category']) as fil_:
					cat = load(fil_)
					cat['descr'][lang] = {'descr': yaml['category'], 'slug':slugify(yaml['category'])}
					#Write category file back with lang
					fil_write = open(app.config["CAT_DIR"] + yaml['category'], "w")
					fil_write.write(dumps(cat))
					fil_write.close()
					app.yasifipo['categories'][yaml['category']][lang] = {'cat': yaml['category'], 'lang': lang,'descr': cat['descr'][lang]['descr'], 'slug': cat['descr'][lang]['slug']}

		if yaml['category'] not in app.yasifipo["cat_ref"].keys():
			app.yasifipo["cat_ref"][yaml['category']] = {}
		if lang not in app.yasifipo["cat_ref"][yaml['category']].keys():
			app.yasifipo["cat_ref"][yaml['category']][lang] = {}
		if type_ not in app.yasifipo["cat_ref"][yaml['category']][lang].keys():
			app.yasifipo["cat_ref"][yaml['category']][lang][type_] = []
		if yaml["ref"] not in app.yasifipo["cat_ref"][yaml['category']][lang][type_]:
			app.yasifipo["cat_ref"][yaml['category']][lang][type_].append(yaml["ref"]) #TODO order ?
