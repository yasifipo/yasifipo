from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from .urls import *
from .langs import *

from modules.site.objects import *

def render_page(file_):

	with open(file_) as data:
		yaml = load(data)

		page = Page('page', yaml)

		page.lang = set_lang(yaml)


		page.langs = get_langs_from_ref(yaml)

		if 'tags' in yaml.keys() and yaml['tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

		if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
			page.display['cucumber'] = True

			if 'parent' in yaml.keys() and 'ref' in yaml.keys():
				page.cucumber = get_page_cucumber(app.yasifipo["refs"][yaml['ref']][page.lang]['file'], page.lang)
			else:
				page.cucumber = []
		else:
			page.cucumber = []

		if 'posts' in yaml.keys() and type(yaml['posts']).__name__ == "bool" and yaml['posts'] == True:
			page.get_posts()
			page.get_full_posts()
		elif 'posts' in yaml.keys() and type(yaml['posts']).__name__ == "int":
			start = request.args.get('page', default= 0, type = int)

			start = page.get_partial_posts(start, yaml['posts'])
			page.get_full_posts()
			prev_url = page.get_prev_url(start, start + yaml['posts'])
			if prev_url:
				page.prev_url = request.base_url + prev_url
			next_url = page.get_next_url(start, start - yaml['posts'])
			if next_url:
				page.next_url = request.base_url + next_url


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
		with open(i['file']) as data_dir:
			yaml_dir = load(data_dir)
			i['url'] = yasifipo_url_for('render_file', path=app.yasifipo["files"][i['file']])
			i['title'] = yaml_dir['title']
			cucumber.append(i)

	return cucumber
