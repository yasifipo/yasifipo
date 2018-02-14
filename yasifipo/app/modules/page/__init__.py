from app import app

from os.path import isfile, isdir, exists
from os import listdir, makedirs

from frontmatter import load
from slugify import slugify

from modules.site import *
from modules.tag import *

def init_page_data():
	if not isdir(app.config['PAGE_DIR']):
		return
	parenting = get_page_data(app.config['PAGE_DIR'], "", [])
	for item in parenting:
		if item[1] not in app.yasifipo["refs"].keys():
			print("WARNING: Parent doesn't exist for file " + item[0])
			continue
		if item[2] not in app.yasifipo["refs"][item[1]].keys():
			print("WARNING: Parenting with bad language for file " + item[0])
			continue
		app.yasifipo["toc"][item[0]] = {}
		app.yasifipo["toc"][item[0]]['type'] = 'page'
		app.yasifipo["toc"][item[0]]['father'] = app.yasifipo["refs"][item[1]][item[2]]['file']


# recursive function
def get_page_data(directory, current_slug, parenting):

	files_ = listdir(directory)

	files = []
	dirs  = []
	statics = []
	static_files = []
	for file_ in files_:
		if isfile(directory + "/" + file_):
			if app.spec.match_file(file_):
				continue
			files.append(file_)
		elif isdir(directory + "/" + file_):
			dirs.append(file_)


	for file_ in files:
		with open(directory + "/" + file_, encoding='utf-8') as fil_:
			yaml = load(fil_)

			if current_slug == "":
				next_slug = slugify(file_)
			else:
				next_slug = current_slug + "/" + slugify(file_)

			#if there is no header on file, create it
			if len(yaml.keys()) == 0:
				with open(directory + "/" + file_, "w", encoding='utf-8') as fil_write:
					fil_write.write('---\n')
					fil_write.write('url: ' + next_slug + "\n")
					fil_write.write('title: ' + file_ + "\n")
					fil_write.write('static: img' + "\n")
					fil_write.write('---\n')
					fil_write.write(yaml.content)

				# create static folder too
				if not exists(directory + "/img/"):
					makedirs(directory + "/img/")

			_serv, _resource = check_server(yaml)
			if _serv == False:
				continue # No resource management for now

			if 'draft' in yaml.keys() and yaml['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			lang = set_lang(yaml)
			if app.yasifipo["langs"][lang]['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue
			set_ref(yaml, directory + "/" + file_)

			# toc
			if 'parent' in yaml.keys():
				item_tmp = []
				item_tmp.append(directory + "/" + file_)
				item_tmp.append(yaml['parent'])
				item_tmp.append(lang)
				parenting.append(item_tmp)

			# no children for pages (for now)

			manage_tags(yaml, "page", directory + "/" + file_)

			if 'url' in yaml.keys():
				if yaml['url'] == "":
					url = '/'
				else:
					url = yaml['url']

				if 'post' in yaml.keys():
					post = yaml['post']
				else:
					post = None
				yasifipo_register('page', url, directory + "/" + file_, {}, post)

				if 'redirect' in yaml.keys():
					reds = []
					if type(yaml['redirect']).__name__ == "str":
						reds.append(yaml['redirect'])
					else:
						reds = yaml['redirect']
					for red in reds:
						yasifipo_register('redirect', red, None, {'url': url})

				# register static folder if needed
				if 'static' in yaml.keys():
					if not exists(directory + "/" + yaml['static'] + "/"):
						makedirs(directory + "/" + yaml['static'] + "/")
					statics.append(yaml['static'])
					register_static_img(directory + "/" + yaml['static'], yaml['url'], yaml['static'])

				# register static files folder if needed
				if 'files' in yaml.keys():
					if not exists(directory + "/" + yaml['files'] + "/"):
						makedirs(directory + "/" + yaml['files'] + "/")
					static_files.append(yaml['files'])
					register_static_img(directory + "/" + yaml['files'], yaml['url'], "")

			else:
				print("WARNING : page without url defined : " + directory + "/" + file_)


	# children directory in current directory
	for file_ in dirs:

		if file_ in statics:
			continue

		if file_ in static_files:
			continue

		# recursive call
		if current_slug == "":
			next_slug = slugify(file_)
		else:
			next_slug = current_slug + "/" + slugify(file_)
		parenting = get_page_data(directory + "/" + file_, next_slug, parenting)

	return parenting
