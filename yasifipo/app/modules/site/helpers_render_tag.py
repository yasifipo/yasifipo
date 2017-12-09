from app import app
from flask import render_template, request

from .__init__ import *

def render_tag(data):
	# retrieve tag description
	tag = {}
	tag['descr'] = app.yasifipo["tags"]["data"][data['tag_type']][data['tag']]['descr'][data['lang']]
	tag['url']   = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["data"][data['tag_type']][data['tag']]['url'][data['lang']])

	# retrieve tag_type description
	tag_type = {}
	tag_type['descr'] = app.yasifipo["tags"]["conf"][data['tag_type']]['descr'][data['lang']]
	tag_type['url']   = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["conf"][data['tag_type']]['urls']['mass'][data['lang']])

	# retrieve other langs for this tag
	langs = get_langs_from_tag(data['tag_type'], data['tag'])

	# retrieve all objects linked to this tag
	objs = []
	#TODO how to sort ?
	for obj in app.yasifipo["tags"]["data"][data['tag_type']][data['tag']]['data'][data['lang']].values():
		item = {}
		with open(obj['file']) as fil_:
			yaml = load(fil_)
			item['title'] = yaml['title']
			item['url']   = yasifipo_url_for('render_file', path=app.yasifipo["files"][obj['file']])
			item['type']  = obj['type'] #TODO type descr
		objs.append(item)


	return render_template('tag/tag.html',
							tag=tag,
							tag_type=tag_type,
							items=objs,
							langs=langs)
