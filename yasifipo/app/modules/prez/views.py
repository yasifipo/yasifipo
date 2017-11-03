from .helpers import *

from modules.site import *

from modules.site.langs import *

from flask import render_template, request
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

			if 'single' in prez.keys():
				with open(app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single']) as prez_:
					yaml_prez = load(prez_)

					if check_server(prez) == False:
						continue

					if 'draft' in prez.keys() and prez['draft'] == True:
						continue

					title = yaml_prez['title']
					list_.append({
						'title': title,
						'url':  yasifipo_url_for('display_prez', file_= app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single'], lang=lang, single=True)
					})

			else:

				with open(app.config['PREZ_DIR'] + prez['slug'] + "/.chapter.md") as prez_:
					yaml_prez = load(prez_)

					if check_server(prez) == False:
						continue

					if 'draft' in prez.keys() and prez['draft'] == True:
						continue

					title = yaml_prez['title']
					list_.append({
						'title': title,
						'url':  yasifipo_url_for('display_chapter', file_= app.config['PREZ_DIR'] + prez['slug'] + "/", up=prez['ref'], lang=lang)
					})

		return render_template('prez/list.html', list_=list_)

# Generate prez page
def display_prez(file_, lang, single):
	with open(file_) as data:
		yaml = load(data)

		category = {}
		cucumber = []
		if 'category' in yaml.keys():
			category['descr'] = app.yasifipo['categories'][yaml['category']][lang]['descr']
			category['url']   = yasifipo_url_for('display_category', category=yaml['category'], lang=lang)

		#TODO lang

		theme = {}
		if 'theme' in yaml.keys():
			theme['theme'] = yasifipo_url_for('static', filename='css/theme/'+yaml['theme']+'.css')
		else:
			theme['theme'] = yasifipo_url_for('static', filename='css/theme/'+ app.config['REVEAL_DEFAULT_THEME'] +'.css')
		theme['reveal_css'] = yasifipo_url_for('static', filename='css/reveal.css')
		theme['conf']   = yasifipo_url_for('static', filename='js/conf.js')


		theme['head'] = yasifipo_url_for('static', filename='lib/js/head.min.js')
		theme['reveal_js'] = yasifipo_url_for('static', filename='js/reveal.js')
		theme['marked'] = yasifipo_url_for('static', filename='plugin/markdown/marked.js')
		theme['markdown'] = yasifipo_url_for('static', filename='plugin/markdown/markdown.js')

		if single == False:
			if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
				cucumber  = get_prez_cucumber(dirname(file_), None, lang)

		return render_template('prez/prez.html', theme=theme, title=yaml['title'], content=img_convert(Markup(yaml.content), request.url_rule.rule), cucumber=cucumber, category=category, own=request.url_rule.rule)





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

	toc_css = yasifipo_url_for('static', filename='css/toc.css')

	return render_template('prez/toc.html', title=yaml['title'], content=Markup(markdown(yaml.content)), toc=Markup(data), display_toc=display_toc, cucumber=cucumber, langs=langs, toc_css=toc_css)
