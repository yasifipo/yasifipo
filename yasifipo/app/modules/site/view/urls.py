from app import app

import sys

from flask import url_for
from flask_frozen import relative_url_for

from modules.site.views import *

from markdown import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

def yasifipo_is_server():
	if len(sys.argv) >= 2 and sys.argv[1] == "freeze":
		return False
	else:
		return True

def yasifipo_url_for(target, **values):
	if yasifipo_is_server() == False:
		return relative_url_for(target, **values)
	else:
		return url_for(target, **values)

class FreezeUrlExtension(Extension):
	def extendMarkdown(self, md, md_globals):
		treeprocessor = FreezeTreeProcessor(md)
		treeprocessor.ext = self
		md.treeprocessors['freeze'] = treeprocessor

class FreezeTreeProcessor(Treeprocessor):

	def run (self, root):
		if yasifipo_is_server() == True:
			return root

		for a in root.iter('a'):
			if a.get("href") == "/":
				a.set("href", yasifipo_url_for('render_root'))
			else:
				if a.get("href")[0] == "/":
					a.set('href', yasifipo_url_for('render_file', path=a.get("href")[1:]))

		return root
