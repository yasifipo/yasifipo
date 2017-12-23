from app import app

from modules.site.view.urls import *
from modules.utils.date import *

from frontmatter import load
from os.path import basename

class TagType():
	def __init__(self, tag_type_, lang_):
		self.tagtype = tag_type_

		self.lang = lang_

		self.description = app.yasifipo["tags"]["conf"][self.tagtype]['descr'][self.lang]
		self.url         = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["conf"][self.tagtype]['urls']['mass'][self.lang])
		self.sort 		 = app.yasifipo["tags"]["conf"][self.tagtype]['sort']

		self.tags = []

	def get_tags(self, tab=None):
		if tab is None:
			for tag_it in app.yasifipo["tags"]["data"][self.tagtype].keys():
				tag = Tag(self.tagtype, tag_it, self.lang)
				self.tags.append(tag)
		else:
			for tag_it in app.yasifipo["tags"]["data"][self.tagtype].keys():
				if tag_it in tab:
					tag = Tag(self.tagtype, tag_it, self.lang)
					self.tags.append(tag)
		self.tags = sorted(self.tags, key=lambda k: k.sort)

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
		self.sort        = app.yasifipo["tags"]["data"][self.type.tagtype][self.tag]['sort']

		self.items = []


	def get_items(self):
		# retrieve all objects linked to this tag
		items = {}
		items_collections = {}
		for obj in app.yasifipo["tags"]["data"][self.type.tagtype][self.tag]['data'][self.lang].values():
			with open(obj['file'], encoding='utf-8') as fil_:
				yaml = load(fil_)
				item = Item(yaml)
				item.title = yaml['title']
				item.type  = obj['type']

				if item.type != "collection":
					item.url   = yasifipo_url_for('render_file', path=app.yasifipo["files"][obj['file']])
					if 'sort' in yaml.keys():
						item.sort = yaml['sort']
					else:
						item.sort = 99

					item.type_description = app.yasifipo["i18n"]["page-type"][item.type][self.lang]
				else:
					if app.yasifipo["collections"][obj['subtype']]['conf']['output_url'] == True:
						item.url   = yasifipo_url_for('render_file', path=app.yasifipo["files"][obj['file']])

					if 'sort' in yaml.keys():
						item.sort = yaml['sort']
					else:
						item.sort = 99

					date, in_, in_2 = get_date(yaml, basename(obj['file']))
					item.date = date

					item.type_description = app.yasifipo["collections"][obj['subtype']]['description'][self.lang]

			if item.type !=  "collection":
				if item.type not in items.keys():
					items[item.type] = ItemType(item.type, app.yasifipo['config']['sorting_item_type'][item.type])
				items[item.type].items.append(item)
			else:
				if item.type not in items_collections.keys():
					#fake only 1 collection, in order to know how to sort
					if obj['subtype'] not in items.keys():
						items[obj['subtype']] = ItemType(item.type, app.yasifipo['config']['sorting_item_type'][item.type], obj['subtype'])
					items[obj['subtype']].items.append(item)
				if obj['subtype'] not in items_collections.keys():
						items_collections[obj['subtype']] = ItemType(item.type, app.yasifipo["collections"][obj['subtype']]['conf']['sort'], obj['subtype'])
				items_collections[obj['subtype']].items.append(item)

		items_list = items.values()
		items_list = sorted(items_list, key=lambda k: k.sort)
		items_collections_list = items_collections.values()
		items_collections_list = sorted(items_collections_list, key=lambda k: k.sort)


		collection_done = False
		for typ_ in items_list:
			if typ_.type != "collection":
				self.items.extend(sorted(typ_.items, key= lambda k: k.sort))
			else:
				if collection_done == False:
					for typ_sub in items_collections_list:
						if app.yasifipo["collections"][obj['subtype']]['conf']['sorting'] == "sort":
							self.items.extend(sorted(typ_sub.items, key= lambda k: k.sort))
						elif app.yasifipo["collections"][obj['subtype']]['conf']['sorting'] == "date":
							tab = sorted(typ_sub.items, key= lambda k: k.date)
							tab.reverse()
							self.items.extend(tab)
				collection_done = True


class ItemType():
	def __init__(self, type_, sort, subtype=None):
		self.type = type_
		self.subtype = subtype
		self.sort = sort
		self.items = []

class Item():
	def __init__(self, yaml):
		self.data = Data(yaml)

class Data():
	def __init__(self, yaml):
		for k in yaml.keys():
			setattr(self, k, yaml[k])
