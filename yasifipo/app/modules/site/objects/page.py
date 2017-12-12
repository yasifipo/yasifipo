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
