from app import app
from datetime import datetime
from modules.utils.date import *

def url_mapping(date, yaml, filename, url):

	if date is None:
		return None

	if 'lang' not in yaml.keys():
		lang = app.yasifipo["config"]["default_lang"]
	else:
		lang = yaml['lang']

	url = url.replace('<year>', str(date.year))
	url = url.replace('<month>', str(date.month))
	url = url.replace('<day>', str(date.day))
	url = url.replace('<lang>', lang)

	return url
