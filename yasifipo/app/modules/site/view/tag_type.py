from app import app
from flask import render_template, request

from .urls import *
from .langs import *

from modules.site.objects import *

def render_tag_type(data):

	page = Page('tag_type')

	page.lang = data['lang']

	page.tag_type = TagType(data['tag_type'], page.lang)

	# retrieve other langs for this tag
	page.langs = get_langs_from_tag_type(data['tag_type'], page.lang)

	page.title = page.tag_type.description

	page.tag_type.get_tags()
	page.tag_type.get_tags_items()
	page.get_generated_time()
	return render_template('tag/tag_type.html',
							site=app.yasifipo["sitedata"],
							i18n=app.yasifipo['i18n'],
							page=page)
