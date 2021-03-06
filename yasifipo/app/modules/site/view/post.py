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

def render_post(file_):
	with open(file_, encoding='utf-8') as data:
		yaml = load(data)

		page = Page('post', yaml)

		page.lang = set_lang(yaml)

		page.app = app

		page.langs = get_langs_from_ref(yaml, page.lang)

		if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
			page.display['tags'] = False
		else:
			if 'display_tags' in app.yasifipo["config"]["default"].keys() and app.yasifipo["config"]["default"]["display_tags"] == False:
				page.display['tags'] = False
			else:
				page.tags_display = page.get_tags_display(yaml)

		page.title   = yaml['title']
		env = Environment()
		env.filters['yasifipo'] = yasifipo
		env.filters['youtube'] = youtube
		env.filters['onlydate'] = onlydate
		env.filters['include'] = include
		env.filters['static'] = static
		page.content = Markup(markdown(env.from_string(pre_filter({'file':file_}, yaml.content)).render(), extensions=app.yasifipo["markdown_process"]))


		if 'layout' in yaml.keys():
			layout = 'post/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_post"]

		get_lists(page, yaml, request)

		post = [ i for i in app.yasifipo["posts"][page.lang] if i['file'] == file_][0] #TODO check perf issue here
		page.post = Post(post['file'], post['date'], page.lang, None)
		page.post.get_prev_next(post['prev'], post['next'])

		page.get_menus(yaml)

	for plugin in app.plugins.values():
		plugin.before_render(page, file_)

	page.get_generated_time()
	return render_template( layout,
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page
							)
