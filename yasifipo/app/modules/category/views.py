from flask import render_template

from .helpers import *

def display_categories(lang):
	return 'TODO'

def display_category(category, lang):

	cat      = {}
	langs    = []
	list_    = []

	cat = {'category': category,
				'descr': app.yasifipo["categories"][category][lang]['descr'],
				'lang': lang
				}

	langs = get_category_langs(category)

	items = get_category_items(category, lang)

	# retrieve type_ sorting & labels
	with open(app.config["CONFIG_DIR"] + "types") as fil_:
		yaml = load(fil_)

		for typ in yaml['types']:
			if typ['name'] in items.keys():
				items[typ['name']]['sort'] = int(typ['sort'])
				items[typ['name']]['descr'] = typ['descr'][lang]

	items = sorted([i for i in items.values()], key=lambda k: k['sort'])

	return render_template('category/category.html', cat=cat, langs=langs, list_=items)
