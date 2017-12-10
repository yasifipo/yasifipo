from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from urls import *
from langs import *

from modules.site.objects import *

def render_page(file_):

	with open(file_) as data:
		yaml = load(data)

		page = Page('page')

		page.lang = set_lang(yaml)

		#TODO tags
		#TODO langs

		if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
			page.display['cucumber'] = True

			if 'parent' in yaml.keys() and 'ref' in yaml.keys():
				page.cucumber = get_page_cucumber(app.yasifipo["refs"][yaml['ref']][page.lang]['file'], page.lang)
			else:
				page.cucumber = []
		else:
			page.cucumber = []


		page.title   = yaml['title']
		page.content = Markup(markdown(yaml.content))

	return render_template('page/page.html',
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
		with open(i['file']) as data_dir:
			yaml_dir = load(data_dir)
			i['url'] = yasifipo_url_for('render_file', path=app.yasifipo["files"][i['file']])
			i['title'] = yaml_dir['title']
			cucumber.append(i)

	return cucumber