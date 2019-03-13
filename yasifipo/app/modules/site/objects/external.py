from app import app

from frontmatter import load

from modules.site.view.urls import *

from .tag import *


class Externals():
	def __init__(self):
		pass

	def set_externals(self, posts):
		self.posts = posts

class External():
	def __init__(self, file_, date, lang, url):
		self.file_ = file_
		self.date  = date
		self.url   = url
		self.next  = None
		self.prev  = None
		self.lang  = lang

	def set_title(self, title):
		self.title = title

	def set_ext_name(self, ext):
		self.ext_name = app.yasifipo["externals"]["conf"][ext]['name'][self.lang]

	def get_prev_next(self, prev, next):
		if prev:
			self.prev = External(prev['file'], prev['date'], self.lang, None)
			self.prev.set_title(prev['title'])
			self.prev.set_ext_name(prev['ext'])
		if next:
			self.next = External(next['file'], next['date'], self.lang, None)
			self.next.set_title(next['title'])
			self.next.set_ext_name(prev['ext'])

	def get_full(self, post):
		pass

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
