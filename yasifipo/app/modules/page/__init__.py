from os.path import isfile, isdir
from os import listdir

from frontmatter import load

from app import app

from .views import *

from modules.site.langs import *
from modules.category import *

# Initialisation of pages data
def init_pages_data():
	app.yasifipo['toc'], app.yasifipo['frozen'] = get_pages_data(app.yasifipo['toc'], app.yasifipo['frozen'], app.config['PAGE_DIR'])


# Main recursive function
def get_pages_data(toc, frozen, directory):

	files = listdir(directory)

	for file_ in files:

		# children directory in current directory
		if isdir(directory + "/" + file_):
			toc, frozen = get_pages_data(toc, frozen, directory + "/" + file_)

		elif isfile(directory + "/" + file_):
			with open(directory + "/" + file_) as fil_:
				yaml = load(fil_)

				#if there is no header on file, create it
				if len(yaml.keys()) == 0:
					with open(directory + "/" + file_, "w") as fil_write:
						fil_write.write('---\n')
						fil_write.write('slug: ' + slugify(file_) + "\n")
						fil_write.write('title: ' + file_ + "\n")
						fil_write.write('---\n')
						fil_write.write(yaml.content)

				if check_server(yaml) == False:
					continue

				if 'draft' in yaml.keys() and yaml['draft'] == True:
					continue

				# toc
				if 'parent' in yaml.keys():
					toc[directory + "/" + file_] = {}
					toc[directory + "/" + file_]['type'] = 'page'
					toc[directory + "/" + file_]['father'] = {}
					toc[directory + "/" + file_]['father']['ref'] = yaml['parent']
					if 'lang' not in yaml.keys():
						lang = app.config['DEFAULT_LANG']
					else:
						lang = yaml['lang']
					toc[directory + "/" + file_]['father']['lang'] = lang

				# no children for pages

				set_lang(yaml)
				set_ref(yaml, directory + "/" + file_)
				manage_category(yaml, "page")
				yasifipo_register(yaml['url'], display_page, 'display_page', {'file_': directory + "/" + file_})

	return toc, frozen
