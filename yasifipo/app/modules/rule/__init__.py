from app import app
from os import listdir
from os.path import isfile, isdir

from frontmatter import load
import pathspec

def init_rules():
	if not isdir(app.config["RULE_DIR"]):
		return
	listfile = listdir(app.config["RULE_DIR"])
	for file_ in listfile:
		if isfile(app.config["RULE_DIR"] + "/" + file_):
			if app.spec.match_file(file_):
				continue
			with open(app.config["RULE_DIR"] + "/" + file_, encoding='utf-8') as fil_data:
				yaml = load(fil_data)

				if 'rule' in yaml.keys():
					if '/' in yaml['func']:
						# from a Plugin
						plugin_value, post_value = yaml['func'].split('/')
						if plugin_value not in app.plugins.keys():
							continue
						if not hasattr(app.plugins[plugin_value], post_value):
							continue
						if not callable(getattr(app.plugins[plugin_value], post_value)):
							continue
						func = getattr(app.plugins[plugin_value], post_value)

						app.add_url_rule(
											rule=yaml['rule'],
											view_func=func,
											defaults={},
											methods=['GET', 'POST']
											)


					else:
						#TODO, no general rules for now
						pass
