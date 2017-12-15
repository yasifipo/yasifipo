from app import app

from os.path import isfile, isdir, exists, splitext
from os import listdir, makedirs
from datetime import datetime

from frontmatter import load
from slugify import slugify

from modules.site import *
from modules.site.objects import *
from modules.tag import *
from .url import *
from .date import *

def init_post_data():
	get_post_data(app.config['POST_DIR'])

	for lang in app.yasifipo["posts"].keys():
		app.yasifipo["posts"][lang] = sorted(app.yasifipo["posts"][lang], key=lambda k: k['date'])
		app.yasifipo["posts"][lang].reverse()
		cpt = 0
		for it in app.yasifipo["posts"][lang]:
			if cpt != 0:
				it['next'] = {'file': app.yasifipo["posts"][lang][cpt-1]['file'], 'date': app.yasifipo["posts"][lang][cpt-1]['date']}
			else:
				it['next'] = None
			if cpt != len(app.yasifipo["posts"][lang])-1:
				it['prev'] = {'file': app.yasifipo["posts"][lang][cpt+1]['file'], 'date': app.yasifipo["posts"][lang][cpt+1]['date']}
			else:
				it['prev'] = None
			cpt += 1

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
					fil_write.write("---\n")
					fil_write.write('date: ' + datetime.now().strftime("%Y%m%d") + "\n")
					fil_write.write('url: ' + app.yasifipo["config"]["post_default_url"] + slugify(os.path.splitext(os.path.basename(file_))[0]) + "\n")
					fil_write.write('title: ' + os.path.splitext(os.path.basename(file_))[0] + "\n")
					fil_write.write('static: img' + "\n")
					fil_write.write("---\n")
					fil_write.write(yaml.content)

				# create static folder too
				if not exists(directory + "/img/"):
					makedirs(directory + "/img/")

				with open(directory + "/" + file_) as fil_:
					yaml = load(fil_)

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

			date, in_key, in_filename = get_date(yaml, file_)
			if date is None:
				print("WARNING: can't get date for file " + file_)
				continue

			if is_in_future(date):
				if app.config['DISPLAY_ALL'] == False:
					continue

			if 'url' in yaml.keys():
				if yaml['url'] == "":
					if app.yasifipo["config"]["post_url_prefix"] == "":
						url = "/"
					else:
						url = app.yasifipo["config"]["post_url_prefix"]
				else:
					if app.yasifipo["config"]["post_url_prefix"] == "":
						url = yaml['url']
					else:
						url = app.yasifipo["config"]["post_url_prefix"] + '/' + yaml['url']
			else:
				# construct default url
				# prefix/<lang>/<year>/<month>/title
				if app.yasifipo["config"]["post_url_prefix"] == "":
					url = app.yasifipo["config"]["post_default_url"]
				else:
					url = app.yasifipo["config"]["post_url_prefix"] + '/' + app.yasifipo["config"]["post_default_url"]

				if in_filename == True:
					url = url + file_[9:len(file_)-len(os.path.splitext(os.path.basename(file_))[1])]
				else:
					url = url + os.path.splitext(file_)[0]

			new_url = url_mapping(date, yaml, file_, url)
			if new_url is None:
				url = url
			else:
				url = new_url

			set_post(lang, directory + "/" + file_, date)
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
				register_static_img(directory + "/" + yaml['static'], url, yaml['static'])



	# children directory in current directory
	for file_ in dirs:

		if file_ in statics:
			continue

		# recursive call
		get_post_data(directory + "/" + file_)

def set_post(lang, file_, date):
	if lang not in app.yasifipo["posts"].keys():
		app.yasifipo["posts"][lang] = []

	app.yasifipo["posts"][lang].append({
									'file': file_,
									'lang': lang,
									'date': date
									})
