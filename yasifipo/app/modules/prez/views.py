from .helpers import *

from modules.site import *

from modules.site.langs import *

from flask import render_template
from flask import Markup

from os.path import dirname
from markdown import markdown

def display_prez_list(lang):
	list_ = []
	with open(app.config['PREZ_DIR'] + "/summary.md") as fil_prez:
		yaml = load(fil_prez)
		for prez in yaml['presentations']:
			if 'lang' not in prez.keys():
				lang_ = app.config['DEFAULT_LANG']
			else:
				lang_ = prez['lang']

			if lang_ != lang:
				continue

			with open(app.config['PREZ_DIR'] + prez['slug'] + "/.chapter.md") as prez_:
				yaml_prez = load(prez_)

				title = yaml_prez['title']
				list_.append({
					'title': title,
					'url':  yasifipo_url_for('display_chapter', file_= app.config['PREZ_DIR'] + prez['slug'] + "/", up=prez['ref'], lang=lang)
				})

		return render_template('prez/list.html', list_=list_)

# Generate prez page
def display_prez(file_, lang):
	with open(file_) as data:
		yaml = load(data)

		if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
			cucumber  = get_prez_cucumber(dirname(file_), None, lang)

		category = {}
		if 'category' in yaml.keys():
			category['descr'] = app.yasifipo['categories'][yaml['category']][lang]['descr']
			category['url']   = yasifipo_url_for('display_category', category=yaml['category'], lang=lang)

		#TODO lang ?

		if 'theme' in yaml.keys():
			theme = url_for('static', filename='css/theme/'+yaml['theme']+'.css')
		else:
			theme = url_for('static', filename='css/theme/'+ app.config['REVEAL_DEFAULT_THEME'] +'.css')

		return render_template('prez/prez.html', theme=theme, title=yaml['title'], content=Markup(yaml.content), cucumber=cucumber, category=category)


# Generate ToC page
def display_chapter(file_, up, lang):
	with open(file_ + "/.chapter.md") as data_file:
		yaml = load(data_file)
		display_toc = True
		data = ""
		if 'display-toc' in yaml.keys() and yaml['display-toc'] == False:
			display_toc = False
		else:
			data = data + "<div class='toc'>"
			data = get_children_data(file_, data, True, lang)
			data = data + "</div>"

	cucumber = []
	if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
		cucumber = get_prez_cucumber(file_, up, lang)

	if up is not None:
		langs = get_langs_from_ref('display_chapter', ref=up, up=up)
	else:
		langs = []
	return render_template('prez/toc.html', title=yaml['title'], content=Markup(markdown(yaml.content)), toc=Markup(data), display_toc=display_toc, cucumber=cucumber, langs=langs)
