from app import app

from os.path import isfile, isdir, exists
from os import listdir, makedirs

from frontmatter import load
from slugify import slugify

from modules.site import *
from modules.tag import *

def init_post_data():
	get_post_data(app.config['POST_DIR'])

# recursive function
def get_post_data(directory):

	files_ = listdir(directory)

	files = []
	dirs  = []
	statics = []
	for file_ in files_:
		if isfile(directory + "/" + file_):
			if app.spec.match_file(file_):
				continue
			files.append(file_)
		elif isdir(directory + "/" + file_):
			dirs.append(file_)


	for file_ in files:
		with open(directory + "/" + file_) as fil_:
			yaml = load(fil_)


			#if there is no header on file, create it
			if len(yaml.keys()) == 0:
				with open(directory + "/" + file_, "w") as fil_write:
					#TODO yaml header
					fil_write.write(yaml.content)

				# create static folder too
				if not exists(directory + "/img/"):
					makedirs(directory + "/img/")

			if check_server(yaml) == False:
				continue

			if 'draft' in yaml.keys() and yaml['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			lang = set_lang(yaml)
			if app.yasifipo["langs"][lang]['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			set_ref(yaml, directory + "/" + file_)
			manage_tags(yaml, "post", directory + "/" + file_)

			if 'url' in yaml.keys():
				if yaml['url'] == "":
					if app.config['POST_URL_PREFIX'] == "":
						url = "/"
					else:
						url = app.config['POST_URL_PREFIX']
				else:
					if app.config['POST_URL_PREFIX'] == "":
						url = yaml['url']
					else:
						url = app.config['POST_URL_PREFIX'] + '/' + yaml['url']
				print(url)
				yasifipo_register('post', url, directory + "/" + file_, {})

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

			else:
				pass
				#TODO construct url based on date & slug


	# children directory in current directory
	for file_ in dirs:

		if file_ in statics:
			continue

		# recursive call
		get_post_data(directory + "/" + file_)
