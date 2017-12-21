from app import app

from frontmatter import load

from modules.site.view.urls import *


class Prezs():
	def __init__(self):
		pass

	def set_prezs(self, prezs):
		self.prezs = prezs

class Prez():
	def __init__(self, file_):
		self.file_ = file_
		self.url   = yasifipo_url_for('render_file', path=app.yasifipo["files"][self.file_])
		self.next  = None
		self.prev  = None

	def get_prev_next(self, prev, next):
		if prev:
			self.prev = Prez(prev['file'])
		if next:
			self.next = Prez(next['file'])

	def get_full(self):
		with open(self.file_, encoding='utf-8') as fil_:
			yaml = load(fil_)

			self.content = yaml.content
			self.title   = yaml['title']
			self.data    = Data(yaml)

class Data():
	def __init__(self, yaml):
		for k in yaml.keys():
			setattr(self, k, yaml[k])
