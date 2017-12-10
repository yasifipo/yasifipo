from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from urls import *
from langs import *

def render_page(file_):

	with open(file_) as data:
		yaml = load(data)

		lang = set_lang(yaml)
		#TODO tags

		if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
			if 'parent' in yaml.keys() and 'ref' in yaml.keys():
				cucumber = get_page_cucumber(app.yasifipo["refs"][yaml['ref']][lang]['file'], lang)
			else:
				cucumber = []
		else:
			cucumber = []


		title=yaml['title']

	return render_template('page/page.html',
							title=title,
							content=Markup(markdown(yaml.content)),
							cucumber=cucumber
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
