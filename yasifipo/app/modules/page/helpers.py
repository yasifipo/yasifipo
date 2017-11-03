from app import app

from modules.site import *

from frontmatter import load

def get_page_cucumber(initial_parent, lang):
	# construct cucumber
	cucumber = []
	urls     = []
	parent = app.yasifipo["refs"][initial_parent][lang]['file']
	while True:
		urls.append({'file':parent})
		if parent in app.yasifipo['toc'].keys() and app.yasifipo['toc'][parent]['father']['ref'] in app.yasifipo["refs"].keys() \
			and lang in app.yasifipo["refs"][app.yasifipo['toc'][parent]['father']['ref']].keys():
			parent = app.yasifipo["refs"][app.yasifipo['toc'][parent]['father']['ref']][lang]['file']
		else:
			break

	for i in reversed(urls):
		with open(i['file']) as data:
			yaml       = load(data)
			i['url']   = yasifipo_url_for('display_page', file_=i['file'])
			i['title'] = yaml['title']
			cucumber.append(i)

	return cucumber
