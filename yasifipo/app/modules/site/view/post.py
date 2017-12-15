from app import app
from flask import render_template

from frontmatter import load
from flask import Markup
from markdown import markdown

from .urls import *
from .langs import *

from modules.site.objects import *

def render_post(file_):
	with open(file_) as data:
		yaml = load(data)

		page = Page('post')

		page.lang = set_lang(yaml)

		page.langs = get_langs_from_ref(yaml)

		if 'tags' in yaml.keys() and yaml['tags'] == False:
			page.display['tags'] = False
		else:
			page.tags_display = page.get_tags_display(yaml)

		page.title   = yaml['title']
		page.content = Markup(markdown(yaml.content, [FreezeUrlExtension()]))

		if 'layout' in yaml.keys():
			layout = 'post/' + yaml['layout']
		else:
			layout = 'post/post.html'

	page.get_generated_time()
	return render_template( layout,
							page=page
							)
