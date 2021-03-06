from app import app

from os.path import isfile, isdir
from os import listdir, makedirs
from os.path import exists

from modules.site import *
from modules.tag import *

from frontmatter import load

from slugify import slugify

def init_prez_data():
	if not isdir(app.config['PREZ_DIR']):
		return
	with open(app.config['PREZ_DIR'] + "/summary.md", encoding='utf-8') as fil_prez:
		yaml = load(fil_prez)
		if not yaml['presentations']:
			return
		for prez in yaml['presentations']:

			_serv, _resource = check_server(prez)
			if _serv == False:
				continue # No resource management for now

			if 'draft' in prez.keys() and prez['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			lang = set_lang(prez)
			if app.yasifipo["langs"][lang]['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			if app.yasifipo["config"]["prez_url_prefix"] == "":
				init_slug = '/'
			else:
				init_slug = "/" + app.yasifipo["config"]["prez_url_prefix"] + "/"

			if 'single' in prez.keys():
				# check if single value is an existing file
				if not isfile(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single']):
					print("ERROR: single file " + prez['single'] + " for prez " + prez['directory'])
					continue

				# register
				with open(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single'], encoding='utf-8') as single_file:
					yaml_single = load(single_file)

					#if there is no header on file, create it
					if len(yaml_single.keys()) == 0:
						with open(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single'], "w", encoding='utf-8') as fil_write:
							fil_write.write('---\n')
							fil_write.write('slug: ' + slugify(prez['single']) + "\n")
							fil_write.write('title: ' + prez['single'] + "\n")
							fil_write.write('---\n')
							fil_write.write(yaml_single.content)

						with open(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single'], encoding='utf-8') as single_file:
							yaml_single = load(single_file)

					if yaml_single['slug'] == '':
						rule = init_slug
					else:
						rule = init_slug + yaml_single['slug'] + "/"


					set_ref(yaml_single, app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single'], lang)

					# register
					yasifipo_register('prez-single', rule, app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single'], {'single':True, 'lang':lang})

					if lang not in app.yasifipo['prezs'].keys():
						app.yasifipo['prezs'][lang] = []
					file_prez = app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single']
					prez_it = {}
					prez_it['file'] = file_prez
					app.yasifipo['prezs'][lang].append(prez_it)


					# redirect
					if 'redirect' in yaml_single.keys():
						reds = []
						if type(yaml_single['redirect']).__name__ == "str":
							reds.append(yaml_single['redirect'])
						else:
							reds = yaml_single['redirect']
						for red in reds:
							yasifipo_register('redirect', red, None, {'url': rule[1:-1]})

					# register static folder if needed
					if 'static' in prez.keys():
						if not exists(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['static'] + "/"):
							makedirs(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['static'] + "/")
						register_static_img(app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['static'], rule[1:-1], prez['static'])

					manage_tags(prez, "prez-single", app.config['PREZ_DIR'] + prez['directory'] + "/" + prez['single'], lang_=lang)

			else:
				manage_tags(prez, "prez-course", app.config['PREZ_DIR']  + prez['directory'] + "/.chapter.md", lang_=lang)

				#recursive stuff
				read_prez_data(app.config['PREZ_DIR']  + prez['directory'] + "/", None, init_slug, lang)

		for lang in app.yasifipo['prezs'].keys():
			app.yasifipo['prezs'][lang].reverse()
			cpt = 0
			for it in app.yasifipo["prezs"][lang]:
				if cpt !=0:
					it['next'] = {'file': app.yasifipo["prezs"][lang][cpt-1]['file'] }
				else:
					it['next'] = None
				if cpt != len(app.yasifipo["prezs"][lang])-1:
					it['prev'] = {'file': app.yasifipo["prezs"][lang][cpt+1]['file'] }
				else:
					it['prev'] = None
				cpt += 1

# Main recursive function for reading prez
def read_prez_data(directory, up_directory, current_slug, lang):
	# current directory
	if not isfile(directory  + '/.chapter.md'):
		#if no .chapter.md --> Create it !
		chapter_ = open(directory  + '/.chapter.md', "w")
		chapter_.write("---\n")
		chapter_.write("slug: " + slugify(directory.split('/')[len(directory.split('/'))-2]) + "\n")
		chapter_.write('title: ' + directory.split('/')[len(directory.split('/'))-2] + "\n")
		chapter_.write('static: img' + "\n")
		chapter_.write("---\n")

		# create static folder too
		if not exists(directory + "/img/"):
			makedirs(directory + "/img/")

	with open(directory  + '/.chapter.md', encoding='utf-8') as chapter_:
		yaml_chapter = load(chapter_)

		# lang warning
		if 'lang' in yaml_chapter.keys():
			print("WARNING: lang will not be taken into account for file " + directory  + '/.chapter.md')

		# toc
		app.yasifipo["toc"][directory + '.chapter.md'] = {}
		app.yasifipo["toc"][directory + '.chapter.md']['type'] = 'prez'
		if up_directory:
			app.yasifipo["toc"][directory + '.chapter.md']['father'] = up_directory + '.chapter.md'
		else:
			app.yasifipo["toc"][directory + '.chapter.md']['father'] = up_directory
		app.yasifipo["toc"][directory + '.chapter.md']['children'] = []

		# rule
		if yaml_chapter['slug']  == '':
			rule = current_slug + slugify(yaml_chapter['slug'])
		else:
			rule = current_slug + slugify(yaml_chapter['slug']) + '/'

		set_ref(yaml_chapter, directory + ".chapter.md" , lang)
		manage_tags(yaml_chapter, "prez-chapter", directory + ".chapter.md", lang_=lang)

		if up_directory:
			yasifipo_register('prez-chapter', rule,  directory  + '.chapter.md', {'type':'prez-chapter', 'lang':lang})
		else:
			yasifipo_register('prez-course', rule,  directory  + '.chapter.md', {'type':'prez-course', 'lang':lang})

			if lang not in app.yasifipo['prezs'].keys():
				app.yasifipo['prezs'][lang] = []
			file_prez = directory  + '.chapter.md'
			prez_it = {}
			prez_it['file'] = file_prez
			app.yasifipo['prezs'][lang].append(prez_it)


		# redirect
		if 'redirect' in yaml_chapter.keys():
			reds = []
			if type(yaml_chapter['redirect']).__name__ == "str":
				reds.append(yaml_chapter['redirect'])
			else:
				reds = yaml_chapter['redirect']
			for red in reds:
				yasifipo_register('redirect', red, None, {'url': rule[1:-1]})


		# register static files if needed
		if 'static' in yaml_chapter.keys():
			if not exists(directory + "/" + yaml_chapter['static'] + "/"):
				makedirs(directory + "/" + yaml_chapter['static'] + "/")
			register_static_img(directory + "/" + yaml_chapter['static'], rule[1:-1], yaml_chapter['static'])
		else:
			yaml_chapter['static'] = ""

	files = listdir(directory)
	for file_ in files:

		# children directory in current directory
		if isdir(directory + "/" + file_) and file_ != yaml_chapter['static']:
			# if .chapter.md does'nt exist --> create it
			if not isfile(directory + "/" + file_ + '/.chapter.md'):
				chapter_ = open(directory + "/" + file_ + '/.chapter.md', "w")
				chapter_.write("---\n")
				chapter_.write("slug: "  + slugify(file_) + "\n")
				chapter_.write('title: ' + file_ + "\n")
				chapter_.write('static: img' + "\n")
				chapter_.write("---\n")

				# create static folder too
				if not exists(directory + "/" + file_ + "/img/"):
					makedirs(directory + "/" + file_ + "/img/")


			with open(directory + "/" + file_ + '/.chapter.md', encoding='utf-8') as chapter_:
				yaml_chapter_dir = load(chapter_)

				# lang warning
				if 'lang' in yaml_chapter_dir.keys():
					print("WARNING: lang will not be taken into account for file " + directory + "/" + file_ + '/.chapter.md')

				# Do not use draft directory
				if 'draft' in yaml_chapter_dir.keys() and yaml_chapter_dir['draft'] == True:
					if app.config['DISPLAY_ALL'] == False:
						continue

			#toc
			app.yasifipo["toc"][directory + '.chapter.md']['children'].append({'type':'dir', 'data':directory + "/" + file_ + "/.chapter.md"})

			new_slug = ""
			if yaml_chapter['slug']  == '':
				new_slug = current_slug + slugify(yaml_chapter['slug'])
			else:
				new_slug = current_slug + slugify(yaml_chapter['slug']) + "/"
			read_prez_data(directory  + "/" + file_ + "/", directory, new_slug, lang)


		# children file in current directory
		elif isfile(directory + "/" + file_) and file_ != ".chapter.md":
			if app.spec.match_file(file_):
				continue
			with open(directory + "/" + file_, encoding='utf-8') as fil_:
				yaml = load(fil_)

				if 'include' in yaml.keys() and yaml['include'] == True:
					continue

				#if there is no header on file, create it
				if len(yaml.keys()) == 0:
					with open(directory + "/" + file_, "w", encoding='utf-8') as fil_write:
						fil_write.write('---\n')
						fil_write.write('slug: ' + slugify(file_) + "\n")
						fil_write.write('title: ' + file_ + "\n")
						fil_write.write('---\n')
						fil_write.write(yaml.content)

				with open(directory + "/" + file_, encoding='utf-8') as fil_:
					yaml = load(fil_)

				# lang warning
				if 'lang' in yaml.keys():
					print("WARNING: lang will not be taken into account for file " + directory + "/" + file_)

				# Do not use draft files
				if 'draft' in yaml.keys() and yaml['draft'] == True:
					if app.config['DISPLAY_ALL'] == False:
						continue

				if up_directory is None:
					if yaml_chapter['slug'] == "":
						rule = current_slug + slugify(yaml['slug']) + "/"
					else:
						rule = current_slug + yaml_chapter['slug'] + "/" + slugify(yaml['slug']) + "/"
				else:
					rule = current_slug + slugify(yaml_chapter['slug']) + "/" + slugify(yaml['slug']) + "/"

				#toc
				app.yasifipo["toc"][directory + ".chapter.md"]['children'].append({'type':'file', 'data':directory + "/" + file_})
				manage_tags(yaml, "prez", directory + "/" + file_, lang_=lang)
				set_ref(yaml, directory + "/" + file_, lang)
				if 'page' in yaml.keys() and yaml['page'] == True:
					yasifipo_register('prez-page', rule, directory + '/' + file_, {'lang':lang})
				else:
					yasifipo_register('prez', rule, directory + '/' + file_, {'lang':lang})

				# redirect
				if 'redirect' in yaml.keys():
					reds = []
					if type(yaml['redirect']).__name__ == "str":
						reds.append(yaml['redirect'])
					else:
						reds = yaml['redirect']
					for red in reds:
						yasifipo_register('redirect', red, None, {'url': rule[1:-1]})

		# This is the file used for current directory data
		elif isfile(directory + "/" + file_) and file_ == ".chapter.md":
			pass
		# static dir
		elif isdir(directory + "/" + file_) and file_ == yaml_chapter['static']:
			pass
		else:
			print("ERROR, something wrong with type of " + directory + "/" + file_)
