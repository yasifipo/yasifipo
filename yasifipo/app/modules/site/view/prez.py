from app import app
from flask import render_template, request

from frontmatter import load
from flask import Markup
from markdown import markdown
from jinja2 import Environment

from os.path import dirname

from .urls import *
from .langs import *
from .list import *

from modules.site.objects import *
from modules.site.view.filters import *

# recursive fonction to construct ToC
def get_children(file_, first_level):
	current = {}
	current['typ'] = 'dir'
	current['first_level'] = first_level
	if first_level == False:
		with open(file_, encoding='utf-8') as data_file:
			yaml = load(data_file)
			current['chapter_url'] = yasifipo_url_for('render_file', path=app.yasifipo["files"][file_])
			current['chapter_title'] = yaml['title']

	if len(app.yasifipo['toc'][file_]['children']) > 0:
		current['children'] = []
	for child in app.yasifipo['toc'][file_]['children']:
		if child['type'] == 'dir':
			current['children'].append(get_children(child['data'], False))
		else:
			with open(child['data'], encoding='utf-8') as data_file:
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
		with open(i['file'], encoding='utf-8') as data_dir:
			yaml_dir = load(data_dir)
			i['url'] = yasifipo_url_for('render_file', path= app.yasifipo["files"][i['file']])
			i['title'] = yaml_dir['title']
			cucumber.append(i)

	return cucumber

def render_prez_chapter(file_, data):
	with open(file_, encoding='utf-8') as data_file:
		yaml = load(data_file)

	page = Page(data['type'], yaml)

	page.display['toc'] = True
	if 'display-toc' in yaml.keys() and yaml['display-toc'] == False:
		page.display['toc'] = False
	else:
		page.toc = get_children(file_, True)

	page.lang = set_lang(yaml, data['lang'])
	page.app = app
	page.langs = get_langs_from_ref(yaml, page.lang)

	if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
		page.display['tags'] = False
	else:
		if 'display_tags' in app.yasifipo["config"]["default"].keys() and app.yasifipo["config"]["default"]["display_tags"] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

	if 'display_cucumber' not in yaml.keys() or ('display_cucumber' in yaml.keys() and yaml['display_cucumber'] != False):
		page.display['cucumber'] = True
		page.cucumber = get_prez_cucumber(file_, page.lang)
	else:
		page.cucumber = []

	page.title = yaml['title']
	env = Environment()
	env.filters['yasifipo'] = yasifipo
	env.filters['youtube'] = youtube
	env.filters['onlydate'] = onlydate
	env.filters['include'] = include
	env.filters['static'] = static
	page.content = Markup(markdown(env.from_string(pre_filter({'file':file_}, yaml.content)).render(), extensions=app.yasifipo["markdown_process"]))

	page.toc_css = yasifipo_url_for('static', filename='css/toc.css')

	get_lists(page, yaml, request)

	page.get_menus(yaml)

	if 'layout' in yaml.keys():
		layout = 'prez/' + yaml['layout']
	else:
		layout = app.yasifipo["config"]["layout_chapter"]

	for plugin in app.plugins.values():
		plugin.before_render(page, file_, data=data)

	page.get_generated_time()
	return render_template(layout,
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page)


def render_prez_prez(file_, data):
	with open(file_, encoding='utf-8') as data_:
		yaml = load(data_)

		if 'single' in data.keys() and data['single'] == True:
			page = Page('prez-single', yaml)
		else:
			page = Page('prez', yaml)

		page.lang = set_lang(yaml, data['lang'])

		page.langs = get_langs_from_ref(yaml, page.lang)

		if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
			page.display['tags'] = False
		else:
			if 'display_tags' in app.yasifipo["config"]["default"].keys() and app.yasifipo["config"]["default"]["display_tags"] == False:
				page.display['tags'] = False
			else:
				page.tags_display = page.get_tags_display(yaml)

		if "default" in app.yasifipo["config"] and "display_sidebar" in app.yasifipo["config"]["default"]:
			page.display['sidebar'] = app.yasifipo["config"]["default"]["display_sidebar"]
		else: # No default in configuration
			page.display['sidebar'] = True

		# Overidde default for sidebar
		if 'display_sidebar' in yaml.keys():
			page.display['sidebar'] = yaml['display_sidebar']

		theme = {}
		if 'theme' in yaml.keys():
			theme['theme'] = yasifipo_url_for('static', filename='css/theme/'+yaml['theme']+'.css')
		else:
			theme['theme'] = yasifipo_url_for('static', filename='css/theme/'+ app.yasifipo["config"]["reveal_default_theme"] +'.css')
		theme['reveal_css'] = yasifipo_url_for('static', filename='css/reveal.css')
		theme['conf']   = yasifipo_url_for('static', filename='js/conf.js')


		theme['head'] = yasifipo_url_for('static', filename='lib/js/head.min.js')
		theme['reveal_js'] = yasifipo_url_for('static', filename='js/reveal.js')
		theme['marked'] = yasifipo_url_for('static', filename='plugin/markdown/marked.js')
		theme['markdown'] = yasifipo_url_for('static', filename='plugin/markdown/markdown.js')

		page.theme = theme

		if 'single' in data.keys() and data['single'] == True:
			page.cucumber = [] # No cucumber for single
		else:
			if 'display_cucumber' not in yaml.keys() or ('display_cucumber' in yaml.keys() and yaml['display_cucumber'] != False):
				page.display['cucumber'] = True
				page.cucumber  = get_prez_cucumber(dirname(file_) + '/.chapter.md', page.lang)
			else:
				page.cucumber = []

		page.title   = yaml['title']

		env = Environment()
		env.filters['yasifipo'] = yasifipo
		env.filters['youtube'] = youtube
		env.filters['onlydate'] = onlydate
		env.filters['include'] = include
		env.filters['static'] = static
		page.content = Markup(env.from_string(pre_filter({'file':file_}, yaml.content)).render())

		get_lists(page, yaml, request)

		page.get_menus(yaml)

		if 'layout' in yaml.keys():
			layout = 'prez/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_prez"]

		for plugin in app.plugins.values():
			plugin.before_render(page, file_, data=data)

		page.get_generated_time()
		return render_template(layout,
								site=app.yasifipo["sitedata"],
								i18n=app.yasifipo['i18n'],
								page=page)

def render_prez_page(file_, data):
	with open(file_, encoding='utf-8') as data_:
		yaml = load(data_)

		page = Page('prez-page', yaml)

		page.lang = set_lang(yaml, data['lang'])

		page.langs = get_langs_from_ref(yaml, page.lang)

		if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
			page.display['tags'] = False
		else:
			if 'display_tags' in app.yasifipo["config"]["default"].keys() and app.yasifipo["config"]["default"]["display_tags"] == False:
				page.display['tags'] = False
			else:
				page.tags_display = page.get_tags_display(yaml)


		if 'display_cucumber' not in yaml.keys() or ('display_cucumber' in yaml.keys() and yaml['display_cucumber'] != False):
			page.display['cucumber'] = True
			page.cucumber  = get_prez_cucumber(dirname(file_) + '/.chapter.md', page.lang)
		else:
			page.cucumber = []

		page.title   = yaml['title']
		env = Environment()
		env.filters['yasifipo'] = yasifipo
		env.filters['youtube'] = youtube
		env.filters['onlydate'] = onlydate
		env.filters['include'] = include
		env.filters['static'] = static
		page.content = Markup(markdown(env.from_string(pre_filter({'file':file_}, yaml.content)).render(), extensions=app.yasifipo["markdown_process"]))

		get_lists(page, yaml, request)

		page.get_menus(yaml)

		if 'layout' in yaml.keys():
			layout = 'prez/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_prez_page"]

		for plugin in app.plugins.values():
			plugin.before_render(page, file_, data=data)

		page.get_generated_time()
		return render_template( layout,
								site=app.yasifipo["sitedata"],
								i18n=app.yasifipo['i18n'],
								page=page)
