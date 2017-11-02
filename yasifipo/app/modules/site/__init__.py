from app import app

from flask import url_for
from flask_frozen import relative_url_for

import sys
import re

def img_convert(text, route):
	if len(sys.argv) >= 2 and sys.argv[1] == "freeze":
		nb = len(route.split('/'))
		prefix = ""
		for i in range(0, nb-1):
			prefix = prefix + "../"
		prefix = prefix[:len(prefix)-1]
		return re.sub(r"\!\[(.*)\]\((.*)\)", r"![\1](" + prefix + r"\2)", text)
	else:
		return text

def yasifipo_url_for(target, **values):
	if len(sys.argv) >= 2 and sys.argv[1] == "freeze":
		return relative_url_for(target, **values)
	else:
		return url_for(target, **values)

def yasifipo_register(rule, view_func, view_func_name, defaults):
	app.add_url_rule(	rule=rule,
						view_func=view_func,
						defaults= defaults)

	app.yasifipo['frozen'].append([view_func_name, defaults])

def set_ref(yaml, file_, lang_=None, up=None):
	if 'ref' in yaml.keys():
		# store ref in order to get all langs of an object
		if yaml["ref"] not in app.yasifipo["refs"].keys():
			app.yasifipo["refs"][yaml["ref"]] = {}
		lang = ''
		if 'lang' not in yaml.keys():
			if lang_ is None:
				lang = app.config['DEFAULT_LANG']
			else:
				lang = lang_
		else:
			lang = yaml['lang']
		app.yasifipo["refs"][yaml["ref"]][lang] = {'lang': lang, 'file':file_, 'up':up}

def check_server(yaml):
	if 'server' in yaml.keys():
		if type(yaml['server']).__name__ == 'str':
			if (yaml['server'] != app.config["YASIFIPO_SERVER"]):
				return False
		elif type(yaml['server']).__name__ == 'list':
			if app.config["YASIFIPO_SERVER"] not in yaml['server']:
				return False
		else:
			return False

	return True
