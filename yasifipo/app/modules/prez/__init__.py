from os.path import isfile, isdir
from os import listdir

from frontmatter import load

from app import app

from .views import *

from modules.site.langs import *
from modules.category import *

from slugify import slugify

# Initialisation of prez data
def init_prez_data():
	with open(app.config['PREZ_DIR'] + "/summary.md") as fil_prez:
		yaml = load(fil_prez)
		for prez in yaml['presentations']:

			if check_server(yaml) == False:
				continue

			if 'draft' in prez.keys() and prez['draft'] == True:
				continue

			set_lang(prez)

			if app.config['PREZ_URL_PREFIX'] == "":
				init_slug = '/'
			else:
				init_slug = "/" + app.config['PREZ_URL_PREFIX'] + "/"

			if 'lang' in prez.keys():
				lang = prez['lang']
			else:
				lang = app.config['DEFAULT_LANG']

			if 'single' in prez.keys():
				# check if single value is an existing file
				if not isfile(app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single']):
					print("ERROR: single file " + prez['single'] + " for prez " + prez['slug'])
					continue

				manage_category(prez, "prez-single", lang)
				set_ref(prez, app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single'])

				# register
				with open(app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single']) as single_file:
					yaml_single = load(single_file)

					#if there is no header on file, create it
					if len(yaml_single.keys()) == 0:
						with open(app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single'], "w") as fil_write:
							fil_write.write('---\n')
							fil_write.write('slug: ' + slugify(prez['single']) + "\n")
							fil_write.write('title: ' + prez['single'] + "\n")
							fil_write.write('---\n')
							fil_write.write(yaml_single.content)


						with open(app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single']) as single_file:
							yaml_single = load(single_file)

					rule = init_slug + yaml_single['slug'] + "/"
					yasifipo_register(rule, display_prez, 'display_prez', {'file_':app.config['PREZ_DIR'] + prez['slug'] + "/" + prez['single'] , 'lang': lang, 'single':True})
			else:

				set_ref(prez, app.config['PREZ_DIR'] + prez['slug'] + "/")
				manage_category(prez, "course", lang)

				if 'ref' in prez.keys():
					ref = prez['ref']
				else:
					ref = None

				# go for recursive stuff
				app.yasifipo['toc'], app.yasifipo['frozen'] = get_prez_data(app.yasifipo['toc'], app.yasifipo['frozen'], app.config['PREZ_DIR']  + prez['slug'] + "/", None, init_slug, ref, lang)


		# register pages for list of prez
		with open(app.config['CONFIG_DIR'] + "/url") as fil_url:
			urls = load(fil_url)

			for lang in urls['prez'].keys():
				yasifipo_register(urls['prez'][lang], display_prez_list, 'display_prez_list', {'lang': lang})



# Main recursive function
def get_prez_data(toc, frozen, directory, up_directory, current_slug, ref, lang):
	# Current directory
	if not isfile(directory  + '/.chapter.md'):
		#if no .chapter.md --> Create it !
		chapter_ = open(directory  + '/.chapter.md', "w")
		chapter_.write("---\n")
		chapter_.write("slug: " + slugify(directory.split('/')[len(directory.split('/'))-2]) + "\n")
		chapter_.write('title: ' + directory.split('/')[len(directory.split('/'))-2] + "\n")
		chapter_.write("---\n")

	with open(directory  + '/.chapter.md') as chapter_:
		yaml_chapter = load(chapter_)

		# toc
		toc[directory] = {}
		toc[directory]['type'] = 'prez'
		toc[directory]['father'] = up_directory
		toc[directory]['children'] = []

		# register
		if yaml_chapter['slug']  == '':
			rule = current_slug + slugify(yaml_chapter['slug'])
		else:
			rule = current_slug + slugify(yaml_chapter['slug']) + '/'

		# used for language at prez up level
		if up_directory is None:
			up   = ref
		else:
			up   = None

		set_ref(yaml_chapter, directory , lang, up)
		manage_category(yaml_chapter, "toc", lang)
		yasifipo_register(rule, display_chapter, 'display_chapter', {'file_': directory, 'up': up, 'lang': lang})

	files = listdir(directory)
	#TODO Exclude some file. Example : saved file with ~
	for file_ in files:

		# children directory in current directory
		if isdir(directory + "/" + file_):
			# if .chapter.md does'nt exist --> create it
			if not isfile(directory + "/" + file_ + '/.chapter.md'):
				chapter_ = open(directory + "/" + file_ + '/.chapter.md', "w")
				chapter_.write("---\n")
				chapter_.write("slug: "  + slugify(file_) + "\n")
				chapter_.write('title: ' + file_ + "\n")
				chapter_.write("---\n")

			with open(directory + "/" + file_ + '/.chapter.md') as chapter_:
				yaml_chapter_dir = load(chapter_)

				# Do not use draft directory
				if 'draft' in yaml_chapter_dir.keys() and yaml_chapter_dir['draft'] == True:
					continue

			#toc
			toc[directory]['children'].append({'type':'dir', 'data':directory + "/" + file_})

			new_slug = ""
			if yaml_chapter['slug']  == '':
				new_slug = current_slug + slugify(yaml_chapter['slug'])
			else:
				new_slug = current_slug + slugify(yaml_chapter['slug']) + "/"
			toc, frozen = get_prez_data(toc, frozen, directory  + "/" + file_, directory, new_slug, ref, lang)

		# children file in current directory
		elif isfile(directory + "/" + file_) and file_ != ".chapter.md":
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

				with open(directory + "/" + file_) as fil_:
					yaml = load(fil_)

				# Do not use draft files
				if 'draft' in yaml.keys() and yaml['draft'] == True:
					continue

				if up_directory is None:
					if yaml_chapter['slug'] == "":
						rule = current_slug + slugify(yaml['slug']) + "/"
					else:
						rule = current_slug + yaml_chapter['slug'] + "/" + slugify(yaml['slug']) + "/"
				else:
					rule = current_slug + slugify(yaml_chapter['slug']) + "/" + slugify(yaml['slug']) + "/"

				#toc
				toc[directory]['children'].append({'type':'file', 'data':directory + "/" + file_})
				manage_category(yaml, "prez", lang)
				set_ref(yaml, directory + "/" + file_, lang)
				yasifipo_register(rule, display_prez, 'display_prez', {'file_': directory + '/' + file_ , 'lang': lang, 'single': False})

		# This is the file used for current directory data
		elif isfile(directory + "/" + file_) and file_ == ".chapter.md":
			pass
		else:
			print("ERROR, something wrong with type of " + directory + "/" + file_)

	return toc, frozen
