from app import app

from os.path import isdir, exists
from os import listdir, makedirs

from frontmatter import load

from modules.site import *
from modules.tag import *
from .url import *
from modules.utils.date import *

def init_collection_data():
	if not isdir(app.config['COLLECTION_DIR']):
		return
	with open(app.config['COLLECTION_DIR'] + "/summary.md", encoding='utf-8') as fil_collection:
		yaml = load(fil_collection)
		if not yaml['collections']:
			return
		for coll in yaml['collections']:

			_serv, _resource = check_server(coll)
			if _serv == False:
				continue #No resource management for now

			if 'draft' in coll.keys() and coll['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			if isdir(app.config['COLLECTION_DIR'] + "/" + coll['directory']):
				app.yasifipo["collections"][coll['slug']] = {}
				app.yasifipo["collections"][coll['slug']]['data'] = {}
				app.yasifipo["collections"][coll['slug']]['description'] = {}

				for lang in coll['description'].keys():
					app.yasifipo["collections"][coll['slug']]['description'][lang] = coll['description'][lang]

				# set configuration for this collection
				app.yasifipo["collections"][coll['slug']]['conf'] = {}
				app.yasifipo["collections"][coll['slug']]['conf']['output_url'] = 'output_url' in coll.keys() and coll['output_url'] == True
				app.yasifipo["collections"][coll['slug']]['conf']['sorting']      = coll['sorting']
				app.yasifipo["collections"][coll['slug']]['conf']['sort']         = coll['sort']

				get_collection_data(app.config['COLLECTION_DIR'] + "/" + coll['directory'], coll)

				# Sorting
				if coll['sorting'] == "date":
					for lang in app.yasifipo["collections"][coll['slug']]['data'].keys():
						app.yasifipo["collections"][coll['slug']]['data'][lang] = sorted(app.yasifipo["collections"][coll['slug']]['data'][lang], key=lambda k: k['date'])
						app.yasifipo["collections"][coll['slug']]['data'][lang].reverse()
						cpt = 0
						for it in app.yasifipo["collections"][coll['slug']]['data'][lang]:
							if cpt != 0:
								it['next'] = {'file': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt-1]['file'], 'date': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt-1]['date']}
							else:
								it['next'] = None
							if cpt != len(app.yasifipo["collections"][coll['slug']]['data'][lang])-1:
								it['prev'] = {'file': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt+1]['file'], 'date': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt+1]['date']}
							else:
								it['prev'] = None
							cpt += 1
				elif coll['sorting'] == "sort":
					for lang in app.yasifipo["collections"][coll['slug']]['data'].keys():
						app.yasifipo["collections"][coll['slug']]['data'][lang] = sorted(app.yasifipo["collections"][coll['slug']]['data'][lang], key=lambda k: k['sort'])
						cpt = 0
						for it in app.yasifipo["collections"][coll['slug']]['data'][lang]:
							if cpt != 0:
								it['next'] = {'file': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt-1]['file'], 'date': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt-1]['date']}
							else:
								it['next'] = None
							if cpt != len(app.yasifipo["collections"][coll['slug']]['data'][lang])-1:
								it['prev'] = {'file': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt+1]['file'], 'date': app.yasifipo["collections"][coll['slug']]['data'][lang][cpt+1]['date']}
							else:
								it['prev'] = None
							cpt += 1

# recursive function
def get_collection_data(directory, yaml_coll):

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
			with open(directory + "/" + file_, encoding='utf-8') as fil_:
				yaml = load(fil_)


				#if there is no header on file, create it
				if len(yaml.keys()) == 0:
					if 'output_url' in yaml_coll.keys() and yaml_coll['output_url'] == True:
						with open(directory + "/" + file_, "w", encoding='utf-8') as fil_write:
							fil_write.write("---\n")
							fil_write.write('date: ' + datetime.now().strftime("%Y%m%d") + "\n")
							fil_write.write('url: ' + app.yasifipo["config"]["post_default_url"] + slugify(os.path.splitext(os.path.basename(file_))[0]) + "\n")
							fil_write.write('title: ' + os.path.splitext(os.path.basename(file_))[0] + "\n")
							fil_write.write('static: img' + "\n")
							if yaml_coll['sorting'] == "sort":
								fil_write.write('sort: 99' + "\n")
							fil_write.write("---\n")
							fil_write.write(yaml.content)
					else:
						with open(directory + "/" + file_, "w", encoding='utf-8') as fil_write:
							fil_write.write("---\n")
							fil_write.write('date: ' + datetime.now().strftime("%Y%m%d") + "\n")
							fil_write.write('title: ' + os.path.splitext(os.path.basename(file_))[0] + "\n")
							fil_write.write('static: img' + "\n")
							if yaml_coll['sorting'] == "sort":
								fil_write.write('sort: 99' + "\n")
							fil_write.write("---\n")
							fil_write.write(yaml.content)

					# create static folder too
					if not exists(directory + "/img/"):
						makedirs(directory + "/img/")

					with open(directory + "/" + file_, encoding='utf-8') as fil_:
						yaml = load(fil_)

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
				manage_tags(yaml, "collection", directory + "/" + file_, subtype_=yaml_coll['slug'])

				date, in_key, in_filename = get_date(yaml, file_)
				if 'output_url' in yaml_coll.keys() and yaml_coll['output_url'] == True:
					if yaml_coll['sorting'] == "date":
						if date is None:
							print("WARNING: can't get date for file " + file_)
							continue

						if is_in_future(date):
							if app.config['DISPLAY_ALL'] == False:
								continue

				if 'output_url' in yaml_coll.keys() and yaml_coll['output_url'] == True:
					if 'url' in yaml.keys():
						if yaml['url'] == "":
							if 'prefix' not in yaml_coll.keys() or yaml_coll['prefix'] == "":
								url = "/"
							else:
								url = yaml_coll['prefix']
						else:
							if 'prefix' not in yaml_coll.keys() or yaml_coll['prefix'] == "":
								url = yaml['url']
							else:
								url = yaml_coll['prefix'] + '/' + yaml['url']
					else:
						# construct default url
						# prefix/<lang>/<year>/<month>/title
						if 'prefix' not in yaml_coll.keys() or yaml_coll['prefix'] == "":
							url = app.yasifipo["config"]["collection_default_url"]
						else:
							url = yaml_coll['prefix'] + '/' + app.yasifipo["config"]["collection_default_url"]

						if in_filename == True:
							url = url + file_[9:len(file_)-len(os.path.splitext(os.path.basename(file_))[1])]
						else:
							url = url + os.path.splitext(file_)[0]

					new_url = url_mapping(date, yaml, file_, url)
					if new_url is None:
						url = url
					else:
						url = new_url

					yasifipo_register('collection', url, directory + "/" + file_, {'collection':yaml_coll['slug']})

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

				if 'sort' in yaml.keys():
					sort = yaml['sort']
				else:
					sort = None
				set_collection(yaml_coll['slug'], lang, directory + "/" + file_, date, sort)


		# children directory in current directory
		for file_ in dirs:

			if file_ in statics:
				continue

			# recursive call
			get_collection_data(directory + "/" + file_, yaml_coll)

def set_collection(slug, lang, file_, date, sort):
	if lang not in app.yasifipo["collections"][slug]['data'].keys():
		app.yasifipo["collections"][slug]['data'][lang] = []

	app.yasifipo["collections"][slug]['data'][lang].append({
									'file': file_,
									'lang': lang,
									'date': date,
									'sort': sort
									})
