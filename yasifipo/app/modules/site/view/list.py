from modules.site.objects import *

def get_lists(page, yaml, request):
	if 'posts' in yaml.keys() and type(yaml['posts']).__name__ == "bool" and yaml['posts'] == True:
		posts = page.get_posts(yaml)
		page.get_full_posts(posts)

		page.posts = Posts()
		page.posts.set_posts(posts)

	elif 'posts' in yaml.keys() and type(yaml['posts']).__name__ == "int":
		start = request.args.get('page', default= 0, type = int)

		start, posts = page.get_partial_posts(start, yaml['posts'], yaml)
		page.get_full_posts(posts)

		page.posts = Posts()
		page.posts.set_posts(posts)

		prev_url = page.get_prev_url('post', start, start + yaml['posts'])
		if prev_url:
			page.posts.prev_url = request.base_url + prev_url
		next_url = page.get_next_url(start, start - yaml['posts'])
		if next_url:
			page.posts.next_url = request.base_url + next_url

	if 'externals' in yaml.keys() and type(yaml['externals']).__name__ == "bool" and yaml['externals'] == True:
		externals = page.get_externals()
		page.get_full_externals(externals)

		page.externals = Externals()
		page.externals.set_externals(externals)

	elif 'externals' in yaml.keys() and type(yaml['externals']).__name__ == "int":
		start = request.args.get('page', default= 0, type = int)

		start, externals = page.get_partial_externals(start, yaml['externals'])
		page.get_full_externals(externals)

		page.externals = Externals()
		page.externals.set_externals(externals)

		prev_url = page.get_prev_url('external', start, start + yaml['externals'])
		if prev_url:
			page.externals.prev_url = request.base_url + prev_url
		next_url = page.get_next_url(start, start - yaml['externals'])
		if next_url:
			page.externals.next_url = request.base_url + next_url

	if 'collections' in yaml.keys():
		for coll in yaml['collections'].keys():
			if type(yaml['collections'][coll]).__name__ == "bool" and yaml['collections'][coll] == True:
				setattr(page, coll, Collection(coll))

				posts = page.get_collection_posts(getattr(page, coll))
				page.get_full_collection_posts(coll, posts)

				getattr(page, coll).set_posts(posts)

			elif type(yaml['collections'][coll]).__name__ == "int":
				start = request.args.get('page', default= 0, type = int)
				setattr(page, coll, Collection(coll))

				start, posts = page.get_partial_collection_posts(getattr(page, coll),start, yaml['collections'][coll])
				page.get_full_collection_posts(coll, posts)

				getattr(page, coll).set_posts(posts)

				prev_url = page.get_prev_url('collection', start, start + yaml['collections'][coll], coll)
				if prev_url:
					getattr(page, coll).prev_url = request.base_url + prev_url
				next_url = page.get_next_url(start, start - yaml['collections'][coll])
				if next_url:
					getattr(page, coll).next_url = request.base_url + next_url

	if 'prezs' in yaml.keys() and type(yaml['prezs']).__name__ == "bool" and yaml['prezs'] == True:
		prezs = page.get_prezs()
		page.get_full_prezs(prezs)

		page.prezs = Prezs()
		page.prezs.set_prezs(prezs)

	elif 'prezs' in yaml.keys() and type(yaml['prezs']).__name__ == "int":
		start = request.args.get('page', default= 0, type = int)

		start, prezs = page.get_partial_prezs(start, yaml['prezs'])
		page.get_full_prezs(prezs)

		page.prezs = Prezs()
		page.prezs.set_prezs(prezs)

		prev_url = page.get_prev_url('prez', start, start + yaml['prezs'])
		if prev_url:
			page.prezs.prev_url = request.base_url + prev_url
		next_url = page.get_next_url(start, start - yaml['prezs'])
		if next_url:
			page.prezs.next_url = request.base_url + next_url

	if 'tags' in yaml.keys() and type(yaml['tags']).__name__ == "bool" and yaml['tags'] == True:
		page.get_tags()
