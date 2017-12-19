from app import app

from modules.site import *

from frontmatter import load
from os.path import isdir
from os import listdir

from slugify import slugify


def manage_tags(yaml, type_, file_, lang_=None, subtype_=None):
	if 'lang' not in yaml.keys():
		if lang_ is None:
			lang = app.yasifipo["config"]["default_lang"]
		else:
			lang = lang_
	else:
		lang = yaml['lang']

	# check if yaml has some slug of tag
	for slug in app.yasifipo["tags"]["conf"].keys():
		if slug not in yaml.keys():
			continue

		# check type
		if type(yaml[slug]).__name__ == 'str':
			tab = [yaml[slug]]
		else:
			tab = yaml[slug]

		for tag in tab:
			# check if this tag already exists
			if tag not in app.yasifipo["tags"]["data"][slug].keys():
				print("new tag '" + tag + "' of type " + slug )
				create_new_tag(tag, slug)

			if lang in app.yasifipo["tags"]["data"][slug][tag]['data'].keys(): #For new lang / draft langs
				app.yasifipo["tags"]["data"][slug][tag]['data'][lang][file_] = {
																			'type': type_,
																			'file': file_,
																			'lang': lang,
																			'subtype': subtype_
																		}


def create_new_tag(tag, tag_type):
	# create new file
	fil_ = open(app.config['TAG_DIR'] + "/" + app.yasifipo["tags"]["conf"][tag_type]['directory'] + "/" + slugify(tag) + ".md", "w")
	fil_.write('---\n')
	fil_.write('slug: ' + tag + '\n')
	fil_.write('sort: 99' + '\n')
	fil_.write('descr:\n')

	for lang in app.yasifipo['langs'].keys():
		fil_.write('  ' + lang +': ' + tag + '\n')

	fil_.write('url:\n')
	for lang in app.yasifipo['langs'].keys():
		fil_.write('  ' + lang +': ' + lang + "/" + tag + '\n')
	fil_.write('---\n')
	fil_.close()

	# fill conf data
	fill_tag_data(slugify(tag) + ".md", tag_type)


def init_tag_data():
	app.yasifipo["tags"]["conf"] = {}
	app.yasifipo["tags"]["data"] = {}

	with open(app.config['TAG_DIR'] + "/summary.md", encoding='utf-8') as fil_tag:
		yaml = load(fil_tag)
		if not yaml['tags']:
			return
		for tag in yaml['tags']:

			app.yasifipo["tags"]["data"][tag['slug']] = {}

			app.yasifipo["tags"]["conf"][tag['slug']] = {}
			app.yasifipo["tags"]["conf"][tag['slug']]['descr'] = {}
			for lang in tag['descr'].keys():
				if app.yasifipo["langs"][lang]["draft"] == True:
					if app.config['DISPLAY_ALL'] == False:
						continue
				app.yasifipo["tags"]["conf"][tag['slug']]['descr'][lang] = tag['descr'][lang]

			app.yasifipo["tags"]["conf"][tag['slug']]['directory'] = tag['directory']

			app.yasifipo["tags"]["conf"][tag['slug']]['sort'] = int(tag['sort'])

			app.yasifipo["tags"]["conf"][tag['slug']]['urls'] = {}

			app.yasifipo["tags"]["conf"][tag['slug']]['urls']['mass'] = {}
			for lang in tag['url']['mass'].keys():
				if app.yasifipo["langs"][lang]["draft"] == True:
					if app.config['DISPLAY_ALL'] == False:
						continue
				app.yasifipo["tags"]["conf"][tag['slug']]['urls']['mass'][lang] = tag['url']['mass'][lang]

			app.yasifipo["tags"]["conf"][tag['slug']]['urls']['url'] = {}
			for lang in tag['url']['url'].keys():
				if app.yasifipo["langs"][lang]["draft"] == True:
					if app.config['DISPLAY_ALL'] == False:
						continue
				app.yasifipo["tags"]["conf"][tag['slug']]['urls']['url'][lang] = tag['url']['url'][lang]

	# register mass urls
	for tag in app.yasifipo["tags"]["conf"].keys():
		for lang in app.yasifipo["tags"]["conf"][tag]["urls"]['mass'].keys():
			if app.yasifipo["langs"][lang]["draft"] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue
			rule = app.yasifipo["tags"]["conf"][tag]["urls"]['mass'][lang]
			yasifipo_register("tag_type", rule, None, {'tag_type': tag, 'lang':lang})

	# reading tag data
	for tag_type in app.yasifipo["tags"]["conf"].keys():
		if not isdir(app.config['TAG_DIR'] + "/" + app.yasifipo["tags"]["conf"][tag_type]['directory']):
			continue

		files = listdir(app.config['TAG_DIR'] + "/" + app.yasifipo["tags"]["conf"][tag_type]['directory'])

		for file_ in files:
			if app.spec.match_file(file_):
				continue
			fill_tag_data(file_, tag_type)


	# register each tag of each tag_type
	for tag_type in app.yasifipo["tags"]["data"].keys():
		for tag in app.yasifipo["tags"]["data"][tag_type].keys():
			for lang in app.yasifipo["tags"]["data"][tag_type][tag]['url'].keys():
				if app.yasifipo["langs"][lang]["draft"] == True:
					if app.config['DISPLAY_ALL'] == False:
						continue
				rule = app.yasifipo["tags"]["data"][tag_type][tag]['url'][lang]
				yasifipo_register("tag", rule, None, {'tag_type': tag_type, 'tag': tag, 'lang': lang })

def fill_tag_data(file_, tag_type):
	with open(app.config['TAG_DIR'] + "/" + app.yasifipo["tags"]["conf"][tag_type]['directory'] + "/" + file_, encoding='utf-8') as fil_tag:
		yaml = load(fil_tag)

		app.yasifipo["tags"]["data"][tag_type][yaml['slug']] = {}

		app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['data'] = {}

		app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['file'] = file_

		app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['sort'] = int(yaml['sort'])

		app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['descr'] = {}
		for lang in	yaml['descr'].keys():
			if app.yasifipo["langs"][lang]["draft"] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue
			app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['descr'][lang] = yaml['descr'][lang]
			app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['data'][lang] = {}

		app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['url'] = {}
		for lang in	yaml['url'].keys():
			if app.yasifipo["langs"][lang]["draft"] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue
			app.yasifipo["tags"]["data"][tag_type][yaml['slug']]['url'][lang] = app.yasifipo["tags"]["conf"][tag_type]['urls']['url'][lang] + "/" + yaml['url'][lang]
