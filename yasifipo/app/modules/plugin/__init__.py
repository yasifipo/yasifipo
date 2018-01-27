from app import app

import sys
import importlib
from os.path import isdir
from os import listdir
from .after_render import *


def init_plugins():
	app.pluginmanager = YasifipoPluginManager(app.config['PLUGIN_DIR'])
	app.yasifipo["markdown_process"].append(AfterRenderExtension())

class YasifipoPlugin():
	def __init__(self):
		pass

	def after_render(self, root):
		# method to be overriden in any plugins
		return root

	def before_render(self, page, file_=None, data={}):
		# method to be overriden in any plugins
		pass

class YasifipoPluginManager():
	def __init__(self, path):
		self.path = path

		if not self.path in sys.path:
			sys.path.insert(0, self.path)

		list_ = listdir(self.path)
		for it in [it_ for it_ in list_ if isdir(self.path + it_)]:
			app.plugins[it] = getattr(importlib.import_module(it), it)()
