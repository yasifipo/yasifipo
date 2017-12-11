from app import app
from flask import render_template, request

from .urls import *
from .langs import *

def render_mass_tag(data):

	# retrieve tag_type description
	tag_type = {}
	tag_type['descr'] = app.yasifipo["tags"]["conf"][data['tag_type']]['descr'][data['lang']]
	tag_type['url']   = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["conf"][data['tag_type']]['urls']['mass'][data['lang']])

	# retrieve other langs for this tag
	langs = get_langs_from_tag_type(data['tag_type'])

	objs = []
	#TODO how to sort ?
	for tag_it in app.yasifipo["tags"]["data"][data['tag_type']].keys():
		tag_type_data = {}
		tag_type_data['title'] = app.yasifipo["tags"]["data"][data['tag_type']][tag_it]['descr'][data['lang']]
		tag_type_data['url']   = yasifipo_url_for('render_file', path=app.yasifipo["tags"]["data"][data['tag_type']][tag_it]['url'][data['lang']])
		tag_type_data['items'] = []
		for obj in app.yasifipo["tags"]["data"][data['tag_type']][tag_it]['data'][data['lang']].values():
			item = {}
			with open(obj['file']) as fil_:
				yaml = load(fil_)
				item['title'] = yaml['title']
				item['url']   = yasifipo_url_for('render_file', path=app.yasifipo["files"][obj['file']])
				item['type']  = obj['type'] #TODO type descr
			tag_type_data['items'].append(item)
		objs.append(tag_type_data)


	return render_template('tag/tag_type.html',
							tag_type=tag_type,
							items=objs,
							langs=langs)

	return 'ok' #TODO
