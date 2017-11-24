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
def get_children(file_, first_level, lang):
	current = {}
	current['typ'] = 'dir'
	current['first_level'] = first_level
	if first_level == False:
		with open(file_ + "/.chapter.md") as data_file:
			yaml = load(data_file)
			current['chapter_url'] = yasifipo_url_for('display_chapter', file_=file_, up=None, lang=lang)
			current['chapter_title'] = yaml['title']

	if len(app.yasifipo['toc'][file_]['children']) > 0:
		current['children'] = []
	for child in app.yasifipo['toc'][file_]['children']:
		if child['type'] == 'dir':
			current['children'].append(get_children(child['data'], False, lang))
		else:
			with open(child['data']) as data_file:
				yaml = load(data_file)
				child_ = {}
				child_['typ'] = 'prez'
				child_['url'] = yasifipo_url_for('display_prez', file_=child['data'], lang=lang, single=False)
				child_['title'] = yaml['title']
				current['children'].append(child_)

	return current

def get_list_of_prez_langs():
	langs = []
	for lang in app.yasifipo["urls"]["prez"].keys():
		if lang in app.yasifipo["langs"]:
			langs.append({'descr':app.yasifipo["langs"][lang]['descr'], 'sort': app.yasifipo["langs"][lang]['sort'], 'url': yasifipo_url_for('display_prez_list', lang=lang)})
	return sorted(langs, key=lambda k: k['sort'])
