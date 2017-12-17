from app import app

from frontmatter import load

from modules.site.view.urls import *


class Collection():
	def __init__(self, name):
		self.name = name

		# retrieve conf for this collection
		if self.name in app.yasifipo["collections"].keys():
			self.url_generated = app.yasifipo["collections"][self.name]['conf']['generate_url']
			self.sorting       = app.yasifipo["collections"][self.name]['conf']['sorting']

	def set_posts(self, posts):
		self.posts = posts

class CollectionPost():
	def __init__(self, file_, date, url=False):
		self.file_ = file_
		self.date  = date
		self.generate_url = url
		if self.generate_url == True:
			self.url   = yasifipo_url_for('render_file', path=app.yasifipo["files"][self.file_])
		self.next  = None
		self.prev  = None

	def get_prev_next(self, prev, next):
		if prev:
			self.prev = CollectionPost(prev['file'], prev['date'], url=self.generate_url)
		if next:
			self.next = CollectionPost(next['file'], next['date'], url=self.generate_url)

	def get_full(self):
		with open(self.file_) as fil_:
			yaml = load(fil_)

			self.content = yaml.content
			self.title   = yaml['title']
			self.data    = Data(yaml)

class Data():
	def __init__(self, yaml):
		for k in yaml.keys():
			setattr(self, k, yaml[k])
