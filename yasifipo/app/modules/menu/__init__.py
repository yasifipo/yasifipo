from app import app
from os import listdir
from os.path import isfile, isdir

from frontmatter import load

import pathspec

def init_menu_data():
	if not isdir(app.config["MENU_DIR"]):
		return
	listfile = listdir(app.config["MENU_DIR"])
	for file_ in listfile:
		if isfile(app.config["MENU_DIR"] + "/" + file_):
			if app.spec.match_file(file_):
				continue
			with open(app.config["MENU_DIR"] + "/" + file_, encoding='utf-8') as fil_data:
				yaml = load(fil_data)

				if 'slug' in yaml.keys():
					app.yasifipo["menu"][yaml['slug']] = {}
					app.yasifipo["menu"][yaml['slug']]['description'] = {}
					for lang in yaml['description'].keys():
						app.yasifipo["menu"][yaml['slug']]['description'][lang] = yaml['description'][lang]
						app.yasifipo["menu"][yaml['slug']]['items'] = []
						for item in yaml['items']:
							it_ = {}
							it_['description'] = {}
							for lang in item['description'].keys():
								it_['description'][lang] = item['description'][lang]
							it_['url'] = {}
							for lang in item['url'].keys():
								it_['url'][lang] = item['url'][lang]
							app.yasifipo["menu"][yaml['slug']]['items'].append(it_)
