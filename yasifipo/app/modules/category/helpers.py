from app import app
from modules.site import *
from frontmatter import load

def get_category_langs(category):
	langs = []
	for lang in app.yasifipo["categories"][category].values():
		langs.append({'descr':app.yasifipo["langs"][lang['lang']]['descr'], 'sort': app.yasifipo["langs"][lang['lang']]['sort'], 'url': yasifipo_url_for('display_category', category=category, lang=lang['lang'] )})
	return sorted(langs, key=lambda k: k['sort'])

def get_categories_langs():
	langs = []
	for lang in app.yasifipo["urls"]["cats"].keys():
		if lang in app.yasifipo["langs"]:
			langs.append({'descr':app.yasifipo["langs"][lang]['descr'], 'sort': app.yasifipo["langs"][lang]['sort'], 'url': yasifipo_url_for('display_categories', lang=lang)})
	return sorted(langs, key=lambda k: k['sort'])

def get_category_items(category, lang):
	items = {}
	if lang not in app.yasifipo["cat_ref"][category].keys():
		return items

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


	# Sorting items in each type
	#TODO
	# for blog --> sorting by date / alphabetically / modif date / sort tag ?
	# for pages --> sorting alphabetically / modif date / sort tag ?
	# for course --> sorting alphabetically / modif date of any file in course / sort tag ?
	# for single prez --> sorting alphabetically / modif date of single prez / sort tag ?
	# for toc --> sorting alphabetically / order in corresponding course / modif date of any file in course / sort tag ?

	return items
