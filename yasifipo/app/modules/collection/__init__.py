

def init_collection_data():
	with open(app.config['COLLECTION_DIR'] + "/summary.md") as fil_collection:
		yaml = load(fil_collection)
		if not yaml['collections']:
			return
		for coll in yaml['collections']:

			if check_server(coll) == False:
				continue

			if 'draft' in coll.keys() and coll['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			lang = set_lang(coll)
			if app.yasifipo["langs"][lang]['draft'] == True:
				if app.config['DISPLAY_ALL'] == False:
					continue

			
