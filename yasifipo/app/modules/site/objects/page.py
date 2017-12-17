from app import app
from flask import request

from datetime import datetime

from .tag import *
from .post import *
from .collection import *

class Page():
	def __init__(self, type_, yaml={}):
		self.type = type_
		self.data = Data(yaml)

		self.title = ''
		self.content = ''
		self.lang = app.yasifipo["config"]["default_lang"]

		self.generated_datetime_ = datetime.now()
		self.generated_datetime = str(self.generated_datetime_)

		self.display = {}
		self.display['cucumber'] = False
		self.display['langs']    = True
		self.display['tags']     = True

		self.collections = {}

	def get_generated_time(self):
		now =  datetime.now()
		delta = now - self.generated_datetime_
		self.generation_time = str(delta.seconds) + "." + str(delta.microseconds)

	def get_tags_display(self, yaml):
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

	def get_posts(self):
		posts = []
		if self.lang not in app.yasifipo["posts"].keys():
			return []
		for post_it in app.yasifipo["posts"][self.lang]:
			post = Post(post_it['file'],post_it['date'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			posts.append(post)
		return posts

	def get_total_post_nb(self):
		return len(app.yasifipo["posts"][self.lang])

	def get_partial_posts(self, start, nb):
		posts = []
		if self.lang not in app.yasifipo["posts"].keys():
			return 0, posts

		if start < 0:
			start = 0

		if start > self.get_total_post_nb():
			start = 0

		if start + nb > self.get_total_post_nb():
			nb = len(app.yasifipo["posts"][self.lang]) - start

		for post_it in app.yasifipo["posts"][self.lang][start:start+nb]:
			post = Post(post_it['file'],post_it['date'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			posts.append(post)

		return start, posts

	def get_prev_url(self, start, end, collection=None):
		if collection is None:
			if end >= self.get_total_post_nb():
				return None
			else:
				text = '?page=' + str(end)
				return text
		else:
			if end >= self.get_total_collection_post_nb(collection):
				return None
			else:
				text = '?page=' + str(end)
				return text

	def get_next_url(self, start, new_start, collection=None):
		if start == 0:
			return None
		if new_start < 0:
			return "?page=0"
		else:
			return "?page=" + str(new_start)

	def get_full_posts(self, posts):
		for post in posts:
			post.get_full()


	def get_collection_posts(self, collection):
		collection_posts  = []
		if collection.name not in app.yasifipo["collections"].keys():
			return []
		if self.lang not in app.yasifipo["collections"][collection.name]['data'].keys():
			return []
		for coll_it in app.yasifipo["collections"][collection.name]['data'][self.lang]:
			coll = CollectionPost(coll_it['file'],coll_it['date'], url=collection.url_generated)
			coll.get_prev_next(coll_it['prev'], coll_it['next'])

			collection_posts.append(coll)
		return collection_posts

	def get_total_collection_post_nb(self, collection):
		return len(app.yasifipo["collections"][collection]['data'][self.lang])

	def get_partial_collection_posts(self, collection, start, nb):
		collection_posts  = []
		if self.lang not in app.yasifipo["collections"][collection.name]['data'].keys():
			return 0, collection_posts

		if start < 0:
			start = 0

		if start > self.get_total_collection_post_nb(collection.name):
			start = 0

		if start + nb > self.get_total_collection_post_nb(collection.name):
			nb = len(app.yasifipo["collections"][collection.name]['data'][self.lang]) - start

		for coll_it in app.yasifipo["collections"][collection.name]['data'][self.lang][start:start+nb]:
			coll = CollectionPost(coll_it['file'],coll_it['date'], url=collection.url_generated)
			coll.get_prev_next(coll_it['prev'], coll_it['next'])

			collection_posts.append(coll)

		return start, collection_posts

	def get_full_collection_posts(self, collection, posts):
		for coll in posts:
			coll.get_full()

class Data():
	def __init__(self, yaml):
		for k in yaml.keys():
			setattr(self, k, yaml[k])
