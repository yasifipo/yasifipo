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

def render_collection(file_, data_):
	with open(file_, encoding='utf-8') as data:
		yaml = load(data)

		page = Page('collection', yaml)

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
			layout = 'collection/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_collection"]

		coll = [ i for i in app.yasifipo["collections"][data_['collection']]['data'][page.lang] if i['file'] == file_][0] #TODO check perf issue here
		page.collection = CollectionPost(coll['file'], coll['date'], page.lang, url=True)
		page.collection.get_prev_next(coll['prev'], coll['next'])

		get_lists(page, yaml, request)

		page.get_menus(yaml)

	for plugin in app.plugins.values():
		plugin.before_render(page, file_, data=data_)

	page.get_generated_time()
	return render_template( layout,
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page
							)
