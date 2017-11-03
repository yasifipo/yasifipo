from flask import render_template

from .helpers import *
from frontmatter import load

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

	items = {}
	for type_ in app.yasifipo["cat_ref"][category][lang].keys():
		for item in app.yasifipo["cat_ref"][category][lang][type_]:
			if type_ in ["course", "toc"]:
				with open(app.yasifipo["refs"][item][lang]['file'] + "/.chapter.md") as fil_:
					yaml = load(fil_)
			else:
				with open(app.yasifipo["refs"][item][lang]['file']) as fil_:
					yaml = load(fil_)

			if type_ not in items.keys():
				items[type_] = {}
				items[type_]['items'] = []

			if type_ == "page":
				items[type_]['items'].append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_page', file_= app.yasifipo["refs"][item][lang]['file'] )})
			elif type_ == "prez":
				items[type_]['items'].append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_prez', file_= app.yasifipo["refs"][item][lang]['file'], lang=lang, single=False )})
			elif type_ == "prez-single":
				items[type_]['items'].append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_prez', file_= app.yasifipo["refs"][item][lang]['file'], lang=lang, single=True )})
			elif type_ == "course":
				items[type_]['items'].append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_chapter', file_= app.yasifipo["refs"][item][lang]['file'], lang=lang)})
			elif type_ == "toc":
				items[type_]['items'].append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_chapter', file_= app.yasifipo["refs"][item][lang]['file'], up=app.yasifipo["refs"][item][lang]['up'], lang=lang)})


	# retrieve type_ sorting & labels
	with open(app.config["CONFIG_DIR"] + "types") as fil_:
		yaml = load(fil_)

		for typ in yaml['types']:
			if typ['name'] in items.keys():
				items[typ['name']]['sort'] = int(typ['sort'])
				items[typ['name']]['descr'] = typ['descr'][lang]

	items = sorted([i for i in items.values()], key=lambda k: k['sort'])

	return render_template('category/category.html', cat=cat, langs=langs, list_=items)
