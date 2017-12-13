from app import app
from flask import render_template, request

from frontmatter import load
from flask import Markup
from markdown import markdown

from os.path import dirname

from .urls import *
from .langs import *


from modules.site.objects import *

# recursive fonction to construct ToC
def get_children(file_, first_level):
	current = {}
	current['typ'] = 'dir'
	current['first_level'] = first_level
	if first_level == False:
		with open(file_) as data_file:
			yaml = load(data_file)
			current['chapter_url'] = yasifipo_url_for('render_file', path=app.yasifipo["files"][file_])
			current['chapter_title'] = yaml['title']

	if len(app.yasifipo['toc'][file_]['children']) > 0:
		current['children'] = []
	for child in app.yasifipo['toc'][file_]['children']:
		if child['type'] == 'dir':
			current['children'].append(get_children(child['data'], False))
		else:
			with open(child['data']) as data_file:
				yaml = load(data_file)
				child_ = {}
				child_['typ'] = 'prez'
				child_['url'] = yasifipo_url_for('render_file', path=app.yasifipo["files"][child['data']])
				child_['title'] = yaml['title']
				current['children'].append(child_)

	return current

def get_prez_cucumber(initial_parent, lang):
	# construct cucumber
	cucumber = []
	urls     = []
	parent = initial_parent
	while parent:
		urls.append({'file':parent})
		if parent in app.yasifipo['toc'].keys():
			parent = app.yasifipo['toc'][parent]['father']
		else:
			#used for 1 level prez
			urls[len(urls)-1]['file'] = urls[len(urls)-1]['file'] + "/"
			break

	for i in reversed(urls):
		with open(i['file']) as data_dir:
			yaml_dir = load(data_dir)
			i['url'] = yasifipo_url_for('render_file', path= app.yasifipo["files"][i['file']])
			i['title'] = yaml_dir['title']
			cucumber.append(i)

	return cucumber

def render_prez_chapter(file_, data):
	with open(file_) as data_file:
		yaml = load(data_file)

	page = Page(data['type'])

	page.display['toc'] = True
	if 'display-toc' in yaml.keys() and yaml['display-toc'] == False:
		page.display['toc'] = False
	else:
		page.toc = get_children(file_, True)

	page.lang = set_lang(yaml)
	page.langs = get_langs_from_ref(yaml)

	if 'tags' in yaml.keys() and yaml['tags'] == False:
		page.display['tags'] = False
	else:
		page.tags_display = page.get_tags_display(yaml)

	if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
		page.display['cucumber'] = True
		page.cucumber = get_prez_cucumber(file_, page.lang)
	else:
		page.cucumber = []

	page.title = yaml['title']
	page.content = Markup(markdown(yaml.content, [FreezeUrlExtension()]))

	page.toc_css = yasifipo_url_for('static', filename='css/toc.css')

	page.get_generated_time()
	return render_template('prez/toc.html',
							page=page)


def render_prez_prez(file_, data):
	with open(file_) as data_:
		yaml = load(data_)

		if 'single' in data.keys() and data['single'] == True:
			page = Page('prez-single')
		else:
			page = Page('prez')

		page.lang = set_lang(yaml)

		page.langs = get_langs_from_ref(yaml)

		if 'tags' in yaml.keys() and yaml['tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

		theme = {}
		if 'theme' in yaml.keys():
			theme['theme'] = yasifipo_url_for('static', filename='css/theme/'+yaml['theme']+'.css')
		else:
			theme['theme'] = yasifipo_url_for('static', filename='css/theme/'+ app.config['REVEAL_DEFAULT_THEME'] +'.css')
		theme['reveal_css'] = yasifipo_url_for('static', filename='css/reveal.css')
		theme['conf']   = yasifipo_url_for('static', filename='js/conf.js')


		theme['head'] = yasifipo_url_for('static', filename='lib/js/head.min.js')
		theme['reveal_js'] = yasifipo_url_for('static', filename='js/reveal.js')
		theme['marked'] = yasifipo_url_for('static', filename='plugin/markdown/marked.js') #TODO to check
		theme['markdown'] = yasifipo_url_for('static', filename='plugin/markdown/markdown.js') #TODO to check

		page.theme = theme

		if 'single' in data.keys() and data['single'] == True:
			page.cucumber = [] # No cucumber for single
		else:
			if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
				page.display['cucumber'] = True
				page.cucumber  = get_prez_cucumber(dirname(file_) + '/.chapter.md', page.lang)
			else:
				page.cucumber = []

		page.title   = yaml['title']
		page.content = Markup(yaml.content)
		page.get_generated_time()
		return render_template('prez/prez.html',
								page=page)

def render_prez_page(file_, data):
	with open(file_) as data_:
		yaml = load(data_)

		page = Page('prez-page')

		page.lang = set_lang(yaml)

		page.langs = get_langs_from_ref(yaml)

		if 'tags' in yaml.keys() and yaml['tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)


		if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
			page.display['cucumber'] = True
			page.cucumber  = get_prez_cucumber(dirname(file_) + '/.chapter.md', page.lang)
		else:
			page.cucumber = []

		page.title   = yaml['title']
		page.content = Markup(markdown(yaml.content, [FreezeUrlExtension()]))
		page.get_generated_time()
		return render_template('prez/page.html',
								page=page)
