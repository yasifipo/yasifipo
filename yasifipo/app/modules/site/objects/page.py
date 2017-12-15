from app import app
from flask import request

from datetime import datetime

from .tag import *
from .post import *

class Page():
	def __init__(self, type_):
		self.type = type_

		self.title = ''
		self.content = ''
		self.lang = app.config['DEFAULT_LANG']

		self.generated_datetime_ = datetime.now()
		self.generated_datetime = str(self.generated_datetime_)

		self.display = {}
		self.display['cucumber'] = False
		self.display['langs']    = True
		self.display['tags']     = True

	def get_generated_time(self):
		now =  datetime.now()
		delta = now - self.generated_datetime_
		self.generation_time = str(delta.seconds) + "." + str(delta.microseconds)

	def get_tags_display(self, yaml):
		items = {}
		for slug in app.yasifipo["tags"]["conf"].keys():
			if slug not in yaml.keys():
				continue
			if not slug in items.keys():
				items[slug] = TagType(slug, self.lang)

		for tagtype in items.values():
			tagtype.get_tags()

		return sorted([i[1] for i in items.items()], key=lambda k: k.sort)

	def get_posts(self):
		self.posts = []
		if self.lang not in app.yasifipo["posts"].keys():
			return
		for post_it in app.yasifipo["posts"][self.lang]:
			post = Post(post_it['file'],post_it['date'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			self.posts.append(post)

	def get_total_post_nb(self):
		return len(app.yasifipo["posts"][self.lang])

	def get_partial_posts(self, start, nb):
		self.posts = []
		if self.lang not in app.yasifipo["posts"].keys():
			return

		if start < 0:
			start = 0

		if start > self.get_total_post_nb():
			start = 0

		if start + nb > self.get_total_post_nb():
			nb = len(app.yasifipo["posts"][self.lang]) - start

		for post_it in app.yasifipo["posts"][self.lang][start:start+nb]:
			post = Post(post_it['file'],post_it['date'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			self.posts.append(post)

		return start

	def get_prev_url(self, start, end):
		if end >= self.get_total_post_nb():
			return None
		else:
			text = '?page=' + str(end)
			return text

	def get_next_url(self, start, new_start):
		if start == 0:
			return None
		if new_start < 0:
			return "?page=0"
		else:
			return "?page=" + str(new_start)

	def get_full_posts(self):
		for post in self.posts:
			post.get_full()
