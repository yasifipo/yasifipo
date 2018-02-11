from app import app
from flask import send_from_directory, redirect, render_template
from flask import request

from .view import *

from modules.request_post.views import *

import os.path

def return_file(id_):
	return send_from_directory(os.path.split(id_)[0], os.path.split(id_)[1])

def render_file(path):
	if app.maintenance == True:
		return render_template('admin/maintenance.html')

	if yasifipo_is_server() and 'yasifipo_subdirectory' in app.yasifipo['config'] and app.yasifipo['config']['yasifipo_subdirectory'] != '':
		if path[:len(app.yasifipo['config']['yasifipo_subdirectory'])] != app.yasifipo['config']['yasifipo_subdirectory']:
			return render_template('site/404.html')
		else:
			path = path[len(app.yasifipo['config']['yasifipo_subdirectory'])+1:]
		if path == "":
			return render_root()

	if path in app.yasifipo["ids"].keys():
		if app.yasifipo["ids"][path]['type'] == "redirect":
			if yasifipo_is_server():
				return redirect(yasifipo_url_for('render_file', path=app.yasifipo["ids"][path]["data"]['url']), code=301)
			else:
				return render_redirection(yasifipo_url_for('render_file', path=app.yasifipo["ids"][path]["data"]['url']))
		elif app.yasifipo["ids"][path]['type'] == "prez-chapter":
			return render_prez_chapter(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "prez-course":
			return render_prez_chapter(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "prez":
			return render_prez_prez(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "prez-page":
			return render_prez_page(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "prez-single":
			return render_prez_prez(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "img":
			return return_file(app.yasifipo["ids"][path]['id'])
		elif app.yasifipo["ids"][path]['type'] == "tag_type":
			return render_tag_type(app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "tag":
			return render_tag(app.yasifipo["ids"][path]["data"])
		elif app.yasifipo["ids"][path]['type'] == "page":
			if request.method == 'GET':
				return render_page(app.yasifipo["ids"][path]['id'])
			elif request.method == 'POST':
				if 'post' not in app.yasifipo["ids"][path].keys():
					return render_template('site/bad_method.html')
				return render_request_post(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]['post'], request)
		elif app.yasifipo["ids"][path]['type'] == "post":
			return render_post(app.yasifipo["ids"][path]['id'])
		elif app.yasifipo["ids"][path]['type'] == "collection":
			return render_collection(app.yasifipo["ids"][path]['id'], app.yasifipo["ids"][path]["data"])
		else:
			return render_template('site/bad_type.html')
	else:
		return render_template('site/404.html'), 404

def render_root():
	if app.maintenance == True:
		return render_template('admin/maintenance.html')
	if app.yasifipo["root"]:
		if app.yasifipo["root"]["type"] == "prez-chapter":
			return render_prez_chapter(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "prez-course":
			return render_prez_chapter(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "prez":
			return render_prez_prez(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "prez-page":
			return render_prez_page(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "prez-single":
			return render_prez_prez(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "img":
			return return_file(app.yasifipo["root"]['id'])
		elif app.yasifipo["root"]["type"] == "tag_type":
			return render_tag_type(app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "tag":
			return render_tag(app.yasifipo["root"]["data"])
		elif app.yasifipo["root"]["type"] == "page":
			return render_page(app.yasifipo["root"]['id'])
		elif app.yasifipo["root"]["type"] == "post":
			return render_post(app.yasifipo["root"]['id'])
		elif app.yasifipo["root"]["type"] == "collection":
			return render_collection(app.yasifipo["root"]['id'], app.yasifipo["root"]["data"])
		else:
			return render_template('site/bad_type.html')
	else:
		return render_template('site/404.html'), 404
