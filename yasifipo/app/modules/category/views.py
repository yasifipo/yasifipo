from flask import render_template

from .helpers import *
from frontmatter import load

def display_categories(lang):
	return 'TODO'

def display_category(category, lang):

	cat      = {}
	langs    = []
	list_    = []

	#TODO category parents

	#TODO check if cat exists
	cat = {'category': category,
				'descr': app.yasifipo["categories"][category][lang]['descr'],
				'lang': lang
				}

	langs = get_category_langs(category)

	items = []
	#TODO sort type_, and get some labels (using a global dict ?)
	for type_ in app.yasifipo["cat_ref"][category][lang].keys():
		for item in app.yasifipo["cat_ref"][category][lang][type_]:
			with open(app.yasifipo["refs"][item][lang]['file']) as fil_:
				yaml = load(fil_)

				if type_ == "page":
					items.append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_page', file_= app.yasifipo["refs"][item][lang]['file'] )})
				elif type_ == "prez":
					print("##")
					print(app.yasifipo["refs"][item][lang]['file'])
					print(lang)
					items.append({ 'title': yaml['title'] , 'url': yasifipo_url_for('display_prez', file_= app.yasifipo["refs"][item][lang]['file'], lang=lang )})
	return render_template('category/category.html', cat=cat, langs=langs, list_=items)
