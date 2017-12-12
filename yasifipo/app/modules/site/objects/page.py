from app import app

from datetime import datetime

from .tag import *

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

	def get_tags(self, yaml):
		self.tags = []
		# check if yaml has some slug of tag
		for slug in app.yasifipo["tags"]["conf"].keys():
			if slug not in yaml.keys():
				continue

			# check type
			if type(yaml[slug]).__name__ == 'str':
				tab = [yaml[slug]]
			else:
				tab = yaml[slug]

			for tag in tab:
				self.tags.append(Tag(slug, tag, self.lang))

	def get_tags_display(self, yaml):
		#TODO how to sort ?
		self.get_tags(yaml)
		items = {}
		for tag in self.tags:
			if not tag.type.tagtype in items.keys():
				items[tag.type.tagtype] = {}
				items[tag.type.tagtype]['tagtype'] 		= tag.type.tagtype
				items[tag.type.tagtype]['description']	= tag.type.description
				items[tag.type.tagtype]['url'] 			= tag.type.url
				items[tag.type.tagtype]['tags'] 		= {}

			items[tag.type.tagtype]['tags'][tag.tag] = {}
			items[tag.type.tagtype]['tags'][tag.tag]['tag']         = tag.tag
			items[tag.type.tagtype]['tags'][tag.tag]['description'] = tag.description
			items[tag.type.tagtype]['tags'][tag.tag]['url']         = tag.url

		return items
