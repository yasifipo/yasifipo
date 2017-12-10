from app import app
from flask import send_from_directory

from .helpers_render_prez import *
from .helpers_render_mass_tag import *
from .helpers_render_tag import *

import os.path

def return_file(id_):
	return send_from_directory(os.path.split(id_)[0], os.path.split(id_)[1])

def render_file(path):
	if path in app.yasifipo["ids"].keys():
		if app.yasifipo["ids"][path]['type'] == "prez-chapter":
			return render_prez_chapter(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "prez":
			return render_prez_prez(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "prez-single":
			return render_prez_prez(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "img":
			return return_file(app.yasifipo["ids"][path]['id'])
		elif app.yasifipo["ids"][path]['type'] == "tag_type":
			return render_mass_tag(app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "tag":
			return render_tag(app.yasifipo["ids"][path]["data"])
		else:
			return 'Bad type' #TODO
	else:
		return '404' #TODO

def render_root():
	if app.yasifipo["root"]:
		if app.yasifipo["root"]["type"] == "prez-chapter":
			return render_prez_chapter(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "prez":
			return render_prez_prez(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "prez-single":
			return render_prez_prez(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "img":
			return return_file(app.yasifipo["root"]['id'])
		elif app.yasifipo["root"]["type"] == "tag_type":
			return render_mass_tag(app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "tag":
			return render_tag(app.yasifipo["root"]["data"])
		else:
			return 'Bad type' #TODO
	else:
		return '404' #TODO
