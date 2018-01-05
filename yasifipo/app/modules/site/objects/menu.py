from app import app

class MenuItem():
	def __init__(self, item, lang):
		self.description = item["description"][lang]
		self.url         = item["url"][lang]

class Menu():
	def __init__(self, slug, lang):
		self.slug = slug
		self.lang = lang

		self.description = app.yasifipo["menu"][self.slug]["description"][self.lang]
		self.items = []
		for item in app.yasifipo["menu"][self.slug]["items"]:
			self.items.append(MenuItem(item, self.lang))
