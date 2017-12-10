from app import app

from os.path import isfile, isdir, exists
from os import listdir, makedirs

from frontmatter import load
from slugify import slugify

from modules.site import *
from modules.tag import *

def init_page_data():
	get_page_data(app.config['PAGE_DIR'], "")

# recursive function
def get_page_data(directory, current_slug):

	files_ = listdir(directory)

	files = []
	dirs  = []
	statics = []
	for file_ in files_:
		if isfile(directory + "/" + file_):
			files.append(file_)
		elif isdir(directory + "/" + file_):
			dirs.append(file_)


	for file_ in files:
		with open(directory + "/" + file_) as fil_:
			yaml = load(fil_)

			if current_slug == "":
				next_slug = slugify(file_)
			else:
				next_slug = current_slug + "/" + slugify(file_)

			#if there is no header on file, create it
			if len(yaml.keys()) == 0:
				with open(directory + "/" + file_, "w") as fil_write:
					fil_write.write('---\n')
					fil_write.write('url: ' + next_slug + "\n")
					fil_write.write('title: ' + file_ + "\n")
					fil_write.write('static: img' + "\n")
					fil_write.write('---\n')
					fil_write.write(yaml.content)

				# create static folder too
				if not exists(directory + "/img/"):
					makedirs(directory + "/img/")

			if check_server(yaml) == False:
				continue

			if 'draft' in yaml.keys() and yaml['draft'] == True:
				continue

			lang = set_lang(yaml)
			set_ref(yaml, directory + "/" + file_)

			# toc
			if 'parent' in yaml.keys():
				app.yasifipo["toc"][directory + "/" + file_] = {}
				app.yasifipo["toc"][directory + "/" + file_]['type'] = 'page'
				app.yasifipo["toc"][directory + "/" + file_]['father'] = app.yasifipo["refs"][yaml['parent']][lang]['file']

			# no children for pages (for now)

			manage_tags(yaml, "page", directory + "/" + file_)

			if 'url' in yaml.keys():
				if yaml['url'] == "":
					url = '/'
				else:
					url = yaml['url']
				yasifipo_register('page', url, directory + "/" + file_, {})

				# register static folder if needed
				if 'static' in yaml.keys():
					statics.append(yaml['static'])
					listfile_static = listdir(directory + "/" + yaml['static'])
					for file_img in listfile_static:
						if yaml['url'] == "":
							rule_ =  "/" + yaml['static'] + "/" + file_img
						else:
							rule_ = "/" + yaml['url'] + "/" + yaml['static'] + "/" + file_img
						yasifipo_register('img', rule_, directory + "/" + yaml['static'] + "/" + file_img)


			else:
				print("WARNING : page without url defined : " + directory + "/" + file_)


	# children directory in current directory
	for file_ in dirs:

		if file_ in statics:
			continue

		# recursive call
		if current_slug == "":
			next_slug = slugify(file_)
		else:
			next_slug = current_slug + "/" + slugify(file_)
		get_page_data(directory + "/" + file_, next_slug)
