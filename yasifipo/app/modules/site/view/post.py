from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from .urls import *
from .langs import *
from .list import *

from modules.site.objects import *

def render_post(file_):
	with open(file_, encoding='utf-8') as data:
		yaml = load(data)

		page = Page('post', yaml)

		page.lang = set_lang(yaml)

		page.langs = get_langs_from_ref(yaml)

		if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

		page.title   = yaml['title']
		page.content = Markup(markdown(yaml.content, [FreezeUrlExtension()]))

		if 'layout' in yaml.keys():
			layout = 'post/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_post"]

		get_lists(page, yaml, request)

		post = [ i for i in app.yasifipo["posts"][page.lang] if i['file'] == file_][0] #TODO check perf issue here
		page.post = Post(post['file'], post['date'])
		page.post.get_prev_next(post['prev'], post['next'])

	page.get_generated_time()
	return render_template( layout,
							site=app.yasifipo["sitedata"],
							page=page
							)
