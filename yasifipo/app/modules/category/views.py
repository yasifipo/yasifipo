from flask import render_template

from .helpers import *

def display_categories(lang):

	cats = {}
	langs = []
	cat = {}

	# retrieve all existing categories
	for categ in app.yasifipo["categories"].values():
		if lang not in categ.keys():
			continue

		cat = {'category': categ[lang]['cat'],
					'descr': categ[lang]['descr'],
					'lang': lang
					}

		items = get_category_items(categ[lang]['cat'], lang)
		if len(items) == 0:
			continue

		cats[categ[lang]['cat']] = {
									'category': cat,
									'items' : items,
									'sort': categ[lang]['sort']
									}

	# retrieve type_ sorting & labels
	with open(app.config["CONFIG_DIR"] + "types") as fil_:
		yaml = load(fil_)

		for cat in cats.values():
			for typ in yaml['types']:
				if typ['name'] in cat['items'].keys():
					cat['items'][typ['name']]['sort'] = int(typ['sort'])
					cat['items'][typ['name']]['descr'] = typ['descr'][lang]

			cat['items'] = sorted([i for i in cat['items'].values()], key=lambda k: k['sort'])

	list_ = sorted([i for i in cats.values()], key=lambda k: k['sort'])

	#TODO langs
	return render_template('category/categories.html', list_=list_)

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
