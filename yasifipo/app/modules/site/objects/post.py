from app import app

from frontmatter import load

from modules.site.view.urls import *

class Post():
	def __init__(self, file_, date):
		self.file_ = file_
		self.date  = date


	def get_full(self):
		with open(self.file_) as fil_:
			yaml = load(fil_)

			self.content = yaml.content
			self.title   = yaml['title']
			self.url     = yasifipo_url_for('render_file', path=app.yasifipo["files"][self.file_])
