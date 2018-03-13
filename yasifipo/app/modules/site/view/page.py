from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown
from jinja2 import Environment

from .urls import *
from .langs import *
from .list import *

from modules.site.objects import *
from modules.site.view.filters import *

def render_page(file_):

	with open(file_, encoding='utf-8') as data:
		yaml = load(data)

		page = Page('page', yaml)

		page.lang = set_lang(yaml)


		page.langs = get_langs_from_ref(yaml, page.lang)

		if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

		if 'display_cucumber' not in yaml.keys() or ('display_cucumber' in yaml.keys() and yaml['display_cucumber'] != False):
			page.display['cucumber'] = True

			if 'parent' in yaml.keys() and 'ref' in yaml.keys():
				page.cucumber = get_page_cucumber(app.yasifipo["refs"][yaml['ref']][page.lang]['file'], page.lang)
			else:
				page.cucumber = []
		else:
			page.cucumber = []

		get_lists(page, yaml, request)


		if 'layout' in yaml.keys():
			layout = 'page/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_page"]

		page.title   = yaml['title']
		env = Environment()
		env.filters['youtube'] = youtube
		page.content = Markup(markdown(env.from_string(yaml.content).render(), app.yasifipo["markdown_process"]))

		page.get_menus(yaml)

	for plugin in app.plugins.values():
		plugin.before_render(page, file_)

	page.get_generated_time()
	return render_template(layout,
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page
							)


def get_page_cucumber(initial_parent, lang):
	# construct cucumber
	cucumber = []
	urls     = []
	parent = initial_parent
	while parent:
		urls.append({'file':parent})
		if parent in app.yasifipo['toc'].keys():
			parent = app.yasifipo['toc'][parent]['father']
		else:

			break


	for i in reversed(urls):
		with open(i['file'], encoding='utf-8') as data_dir:
			yaml_dir = load(data_dir)
			i['url'] = yasifipo_url_for('render_file', path=app.yasifipo["files"][i['file']])
			i['title'] = yaml_dir['title']
			cucumber.append(i)

	return cucumber
