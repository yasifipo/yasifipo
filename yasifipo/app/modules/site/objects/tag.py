from app import app

from modules.site.view.urls import *

from frontmatter import load

class TagType():
	def __init__(self, tag_type_, lang_):
		self.tagtype = tag_type_

		self.lang = lang_

		self.description = app.yasifipo["tags"]["conf"][self.tagtype]['descr'][self.lang]
		self.url         = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["conf"][self.tagtype]['urls']['mass'][self.lang])

		self.tags = []

	def get_tags(self):
		#TODO how to sort ?
		for tag_it in app.yasifipo["tags"]["data"][self.tagtype].keys():
			tag = Tag(self.tagtype, tag_it, self.lang)
			self.tags.append(tag)

	def get_tags_items(self):
		for tag in self.tags:
			tag.get_items()

class Tag():
	def __init__(self, tag_type_, tag_, lang_):
		self.type = TagType(tag_type_, lang_)
		self.tag  = tag_

		self.lang = lang_

		self.description = app.yasifipo["tags"]["data"][self.type.tagtype][self.tag]['descr'][self.lang]
		self.url         = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["data"][self.type.tagtype][self.tag]['url'][self.lang])

		self.items = []


	def get_items(self):
		# retrieve all objects linked to this tag
		#TODO how to sort ?
		for obj in app.yasifipo["tags"]["data"][self.type.tagtype][self.tag]['data'][self.lang].values():
			item = Item()
			with open(obj['file']) as fil_:
				yaml = load(fil_)
				item.title = yaml['title']
				item.url   = yasifipo_url_for('render_file', path=app.yasifipo["files"][obj['file']])
				item.type  = obj['type']
				item.type_description = app.yasifipo["i18n"]["page-type"][item.type][self.lang]
			self.items.append(item)

class Item():
	def __init__(self):
		pass
