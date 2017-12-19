from app import app

from os.path import isfile, splitext, basename
from os import listdir
from frontmatter import load
from slugify import slugify



class SiteDateFile():
	def __init__(self, file_):
		with open(file_, encoding='utf-8') as fil_data:
			yaml = load(fil_data)

			for key in yaml.keys():
				if type(yaml[key]).__name__ == "list":
					tab = []
					for it in yaml[key]:
						tab.append(it)
					setattr(self, key, tab)
				else:
					setattr(self, key, yaml[key])

class SiteData():
	def __init__(self, directory):
		listfile = listdir(directory)
		for file_ in listfile:
			if isfile(app.config["SITEDATA_DIR"] + "/" + file_):
				if app.spec.match_file(file_):
					continue
				attr_name = splitext(basename(file_))[0]
				setattr(self, attr_name, SiteDateFile(app.config["SITEDATA_DIR"] + "/" + file_))
