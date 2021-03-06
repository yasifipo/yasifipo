from app import app
from flask import request

from datetime import datetime
from frontmatter import load

from .tag import *
from .post import *
from .external import *
from .collection import *
from .prez import *
from .menu import *
from ..view.filters import yasifipo, static

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

	def get_posts(self, yaml):
		posts = []
		if self.lang not in app.yasifipo["posts"].keys():
			return []
		for post_it in app.yasifipo["posts"][self.lang]:

			# check if there is some filter
			if 'filter' in yaml.keys():
				keep_it = False
				for tag_type in yaml['filter'].keys():
					if tag_type in app.yasifipo['tags']['data'].keys():
						if post_it['file'] in app.yasifipo['tags']['data'][tag_type][yaml['filter'][tag_type]]['data'][self.lang].keys():
							keep_it = True
							break
			else:
				keep_it = True

			if keep_it is False:
				continue

			post = Post(post_it['file'],post_it['date'], self.lang, post_it['resource'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			posts.append(post)
		return posts

	def get_externals(self):
		posts = []
		if self.lang not in app.yasifipo["externals"]["data"]["posts"].keys():
			return []
		for post_it in app.yasifipo["externals"]["data"]["posts"][self.lang]:
			post = External(post_it['file'], post_it['date'], self.lang, post_it['url'])
			post.set_title(post_it['title'])
			post.set_ext_name(post_it['ext'])
			post.get_prev_next(post_it['prev'], post_it['next'])
			posts.append(post)
		return posts

	def get_collection_posts(self, collection):
		collection_posts  = []
		if collection.name not in app.yasifipo["collections"].keys():
			return []
		if self.lang not in app.yasifipo["collections"][collection.name]['data'].keys():
			return []
		for coll_it in app.yasifipo["collections"][collection.name]['data'][self.lang]:
			coll = CollectionPost(coll_it['file'],coll_it['date'], self.lang, url=collection.url_generated)
			coll.get_prev_next(coll_it['prev'], coll_it['next'])

			collection_posts.append(coll)
		return collection_posts

	def get_prezs(self):
		prezs = []

		if self.lang not in app.yasifipo['prezs'].keys():
			return []

		for prez_it in app.yasifipo['prezs'][self.lang]:
			prez = Prez(prez_it['file'])
			prez.get_prev_next(prez_it['prev'], prez_it['next'])

			prezs.append(prez)

		return prezs


	def get_total_post_nb(self):
		if self.lang not in app.yasifipo["posts"].keys():
			return 0
		return len(app.yasifipo["posts"][self.lang])

	def get_total_external_nb(self):
		if self.lang not in app.yasifipo["externals"]["data"]["posts"].keys():
			return 0
		return len(app.yasifipo["externals"]["data"]["posts"][self.lang])

	def get_total_collection_post_nb(self, collection):
		if self.lang not in app.yasifipo["collections"][collection]['data'].keys():
			return 0
		return len(app.yasifipo["collections"][collection]['data'][self.lang])

	def get_total_prezs_nb(self):
		if self.lang not in app.yasifipo["prezs"].keys():
			return 0
		return len(app.yasifipo["prezs"][self.lang])

	def get_partial_externals(self, start, nb):
		posts = []
		if self.lang not in app.yasifipo["externals"]["data"]["posts"].keys():
			return 0, posts

		if start < 0:
			start = 0

		if start >= self.get_total_external_nb():
			start = 0

		if start + nb > self.get_total_external_nb():
			nb = len(app.yasifipo["externals"]["data"]["posts"][self.lang]) - start

		for post_it in app.yasifipo["externals"]["data"]["posts"][self.lang][start:start+nb]:
			post = External(post_it['file'],post_it['date'], self.lang, post_it['resource'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			posts.append(post)

		return start, posts

	def get_partial_posts(self, start, nb, yaml):
		posts = []
		if self.lang not in app.yasifipo["posts"].keys():
			return 0, posts

		if start < 0:
			start = 0

		if start >= self.get_total_post_nb():
			start = 0

		if start + nb > self.get_total_post_nb():
			nb = len(app.yasifipo["posts"][self.lang]) - start

		for post_it in app.yasifipo["posts"][self.lang][start:start+nb]:


			# check if there is some filter
			if 'filter' in yaml.keys():
				keep_it = False
				for tag_type in yaml['filter'].keys():
					if tag_type in app.yasifipo['tags']['data'].keys():
						if post_it['file'] in app.yasifipo['tags']['data'][tag_type][yaml['filter'][tag_type]]['data'][self.lang].keys():
							keep_it = True
							break

			else:
				keep_it = True

			if keep_it is False:
				continue

			post = Post(post_it['file'],post_it['date'], self.lang, post_it['resource'])
			post.get_prev_next(post_it['prev'], post_it['next'])

			posts.append(post)

		return start, posts

	def get_partial_collection_posts(self, collection, start, nb):
		collection_posts  = []
		if self.lang not in app.yasifipo["collections"][collection.name]['data'].keys():
			return 0, collection_posts

		if start < 0:
			start = 0

		if start >= self.get_total_collection_post_nb(collection.name):
			start = 0

		if start + nb > self.get_total_collection_post_nb(collection.name):
			nb = len(app.yasifipo["collections"][collection.name]['data'][self.lang]) - start

		for coll_it in app.yasifipo["collections"][collection.name]['data'][self.lang][start:start+nb]:
			coll = CollectionPost(coll_it['file'],coll_it['date'], self.lang, url=collection.url_generated)
			coll.get_prev_next(coll_it['prev'], coll_it['next'])

			collection_posts.append(coll)

		return start, collection_posts

	def get_partial_prezs(self, start, nb):
		prezs  = []
		if self.lang not in app.yasifipo['prezs'].keys():
			return []

		if start < 0:
			start = 0

		if start >= self.get_total_prezs_nb():
			start = 0

		if start + nb > self.get_total_prezs_nb():
			nb = len(app.yasifipo["prezs"][self.lang]) - start

		for prez_it in app.yasifipo["prezs"][self.lang][start:start+nb]:
			prez = Prez(prez_it['file'])
			prez.get_prev_next(prez_it['prev'], prez_it['next'])

			prezs.append(prez)

		return start, prezs


	def get_prev_url(self, type_, start, end, collection=None):
		if type_ == 'post':
			if end >= self.get_total_post_nb():
				return None
			else:
				text = '?page=' + str(end)
				return text
		elif type_ == 'external':
			if end>= self.get_total_external_nb():
				return None
			else:
				text = '?page=' + str(end)
				return text
		elif type_ == 'collection':
			if end >= self.get_total_collection_post_nb(collection):
				return None
			else:
				text = '?page=' + str(end)
				return text
		elif type_ == 'prez':
			if end >= self.get_total_prezs_nb():
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

	def get_full_posts(self, posts):
		for post in posts:
			post.get_full()

	def get_full_externals(self, posts):
		for post in posts:
			post.get_full(post)

	def get_full_collection_posts(self, collection, posts):
		for coll in posts:
			coll.get_full()

	def get_full_prezs(self, prezs):
		for prez in prezs:
			prez.get_full()

	def get_tags(self):
		self.tags = []
		for i in app.yasifipo["tags"]["conf"].keys():
			tag_type = TagType(i, self.lang)

			tag_type.get_tags()
			tag_type.get_tags_items()

			self.tags.append(tag_type)
		self.tags = sorted(self.tags, key=lambda k: k.sort)

	def get_menus(self, yaml):
		self.menus = []
		if "menu" in yaml.keys():
			menus = []
			if type(yaml['menu']).__name__ == "str":
				menus.append(yaml['menu'])
			else:
				menus = yaml['menu']
			for menu in menus:
				self.menus.append(Menu(menu, self.lang))

		# Convert url if needed, using yasifipo filter or static filter
		for menu in self.menus:
			for item in menu.items:
				try:
					text = item.url.split("{{")[1]
					tab = text.split("|")
					if "yasifipo" in tab[1]:
						item.url = yasifipo(tab[0][1:-1])
					elif "static" in tab[1]:
						item.url = static(tab[0][1:-1])
				except:
					pass # If this is a "normal" url

class Data():
	def __init__(self, yaml):
		for k in yaml.keys():
			setattr(self, k, yaml[k])
