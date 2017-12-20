from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from .urls import *
from .langs import *
from .list import *

from modules.site.objects import *

def render_page(file_):

	with open(file_, encoding='utf-8') as data:
		yaml = load(data)

		page = Page('page', yaml)

		page.lang = set_lang(yaml)


		page.langs = get_langs_from_ref(yaml)

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
		page.content = Markup(markdown(yaml.content, [FreezeUrlExtension()]))

	page.get_generated_time()
	return render_template(layout,
							site=app.yasifipo["sitedata"],
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
