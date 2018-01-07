from app import app

from modules.site import *


class YasifipoApi():
	def __init__(self):
		pass

# register some function to be used in plugins
		setattr(self, "url_for", yasifipo_url_for)

def init_api():
	app.api = YasifipoApi()
