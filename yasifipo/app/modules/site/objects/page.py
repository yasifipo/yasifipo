from app import app

class Page():
	def __init__(self, type_):
		self.type = type_

		self.title = ''
		self.content = ''
		self.lang = app.config['DEFAULT_LANG']

		self.generated_datetime = None #TODO

		self.display = {}
		self.display['cucumber'] = False
		self.display['langs']    = False
		self.display['tags']     = False
