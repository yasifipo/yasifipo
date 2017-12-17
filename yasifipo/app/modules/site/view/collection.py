from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from .urls import *
from .langs import *

from modules.site.objects import *

def render_collection(file_, data_):
	with open(file_) as data:
		yaml = load(data)

		page = Page('collection', yaml)

		page.lang = set_lang(yaml)

		page.langs = get_langs_from_ref(yaml)

		if 'tags' in yaml.keys() and yaml['tags'] == False:
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
		page.collection = CollectionPost(coll['file'], coll['date'], url=True)
		page.collection.get_prev_next(coll['prev'], coll['next'])

	page.get_generated_time()
	return render_template( layout,
							site=app.yasifipo["sitedata"],
							page=page
							)
