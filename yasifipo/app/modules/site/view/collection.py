from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from .urls import *
from .langs import *
from .list import *

from modules.site.objects import *

def render_collection(file_, data_):
	with open(file_, encoding='utf-8') as data:
		yaml = load(data)

		page = Page('collection', yaml)

		page.lang = set_lang(yaml)

		page.langs = get_langs_from_ref(yaml, page.lang)

		if 'display_tags' in yaml.keys() and yaml['display_tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

		page.title   = yaml['title']
		page.content = Markup(markdown(yaml.content, [FreezeUrlExtension()]))

		if 'layout' in yaml.keys():
			layout = 'collection/' + yaml['layout']
		else:
			layout = app.yasifipo["config"]["layout_collection"]

		coll = [ i for i in app.yasifipo["collections"][data_['collection']]['data'][page.lang] if i['file'] == file_][0] #TODO check perf issue here
		page.collection = CollectionPost(coll['file'], coll['date'], page.lang, url=True)
		page.collection.get_prev_next(coll['prev'], coll['next'])

		get_lists(page, yaml, request)

		page.get_menus(yaml)

	page.get_generated_time()
	return render_template( layout,
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page
							)
