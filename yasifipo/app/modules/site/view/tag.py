from app import app
from flask import render_template, request

from .urls import *
from .langs import *

from modules.site.objects import *

def render_tag(data):

	page = Page('tag')

	page.lang = data['lang']

	page.app = app

	page.tag = Tag(data['tag_type'], data['tag'], page.lang)

	page.title = page.tag.description

	# retrieve other langs for this tag
	page.langs = get_langs_from_tag(data['tag_type'], data['tag'], page.lang)

	page.tag.get_items()

	for plugin in app.plugins.values():
		plugin.before_render(page, None, data=data)

	page.get_generated_time()
	return render_template('tag/tag.html',
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page)
