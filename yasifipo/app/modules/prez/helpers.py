from app import app

from frontmatter import load

from modules.site import *


def get_prez_cucumber(initial_parent, ref, lang):
	# construct cucumber
	cucumber = []
	urls     = []
	parent = initial_parent
	while parent:
		urls.append({'file':parent})
		if parent in app.yasifipo['toc'].keys():
			parent = app.yasifipo['toc'][parent]['father']
		else:
			#used for 1 level prez
			urls[len(urls)-1]['file'] = urls[len(urls)-1]['file'] + "/"
			break

	up = ref
	for i in reversed(urls):
		with open(i['file'] + "/.chapter.md") as data_dir:
			yaml_dir = load(data_dir)
			i['url'] = yasifipo_url_for('display_chapter', file_= i['file'], up=up, lang=lang)
			i['title'] = yaml_dir['title']
			cucumber.append(i)
		up = None

	return cucumber



# recursive fonction to construct ToC
def get_children_data(file_, data, first_level, lang):
	if first_level == False:
		data = data + "<li>"
		with open(file_ + "/.chapter.md") as data_file:
			yaml = load(data_file)
			data = data + "<a href='" + yasifipo_url_for('display_chapter', file_=file_, up=None, lang=lang)  +"'>" + yaml['title'] + "</a>"

	data = data + "<ol>"
	for child in app.yasifipo['toc'][file_]['children']:
		if child['type'] == 'dir':
			data = get_children_data(child['data'], data, False, lang)
		else:
			data = data + "<li>"
			with open(child['data']) as data_file:
				yaml = load(data_file)
				data = data + "<a href='" + yasifipo_url_for('display_prez', file_=child['data'], lang=lang)  +"'>" + yaml['title'] + "</a>"
			data = data + "</li>"
	data = data + "</ol>"

	if first_level == False:
		data = data + "</li>"

	return data
