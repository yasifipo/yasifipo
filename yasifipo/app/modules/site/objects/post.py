from app import app

from frontmatter import load

from modules.site.view.urls import *

from .tag import *


class Posts():
	def __init__(self):
		pass

	def set_posts(self, posts):
		self.posts = posts

class Post():
	def __init__(self, file_, date, lang, resource):
		self.file_ = file_
		self.date  = date
		self.resource = (resource is not None)
		if not self.resource:
			self.url   = yasifipo_url_for('render_file', path=app.yasifipo["files"][self.file_])
		else:
			self.url = resource
		self.next  = None
		self.prev  = None
		self.lang  = lang

	def get_prev_next(self, prev, next):
		if prev:
			self.prev = Post(prev['file'], prev['date'], self.lang, None)
		if next:
			self.next = Post(next['file'], next['date'], self.lang, None)

	def get_full(self):
		with open(self.file_, encoding='utf-8') as fil_:
			yaml = load(fil_)

			self.content = yaml.content
			self.title   = yaml['title']
			self.data    = Data(yaml)
			self.display_tags = self.get_display_tags(yaml)

	def get_display_tags(self, yaml):
		items = {}
		for slug in app.yasifipo["tags"]["conf"].keys():
			if slug not in yaml.keys():
				continue
			if slug not in items.keys():
				items[slug] = TagType(slug, self.lang)


		for tagtype in items.values():
			if type(yaml[tagtype.tagtype]).__name__ == "str":
				tab = [yaml[tagtype.tagtype]]
			else:
				tab = yaml[tagtype.tagtype]
			tagtype.get_tags(tab)

		return sorted([i[1] for i in items.items()], key=lambda k: k.sort)

class Data():
	def __init__(self, yaml):
		for k in yaml.keys():
			setattr(self, k, yaml[k])
