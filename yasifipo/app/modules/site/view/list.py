from modules.site.objects import *

def get_lists(page, yaml, request):
	if 'posts' in yaml.keys() and type(yaml['posts']).__name__ == "bool" and yaml['posts'] == True:
		page.get_posts()
		page.get_full_posts()

		page.posts = Posts()
		page.posts.set_posts(page.tmp_posts)
		del page.tmp_posts

	elif 'posts' in yaml.keys() and type(yaml['posts']).__name__ == "int":
		start = request.args.get('page', default= 0, type = int)

		start = page.get_partial_posts(start, yaml['posts'])
		page.get_full_posts()

		page.posts = Posts()
		page.posts.set_posts(page.tmp_posts)
		del page.tmp_posts

		prev_url = page.get_prev_url(start, start + yaml['posts'])
		if prev_url:
			page.posts.prev_url = request.base_url + prev_url
		next_url = page.get_next_url(start, start - yaml['posts'])
		if next_url:
			page.posts.next_url = request.base_url + next_url

	if 'collections' in yaml.keys():
		for coll in yaml['collections'].keys():
			if type(yaml['collections'][coll]).__name__ == "bool" and yaml['collections'][coll] == True:
				setattr(page, coll, Collection(coll))

				page.get_collection_posts(getattr(page, coll))
				page.get_full_collection_posts(coll)

				getattr(page, coll).set_posts(page.collections[coll])

			elif type(yaml['collections'][coll]).__name__ == "int":
				start = request.args.get('page', default= 0, type = int)

				start = page.get_partial_collection_posts(coll,start, yaml['collections'][coll])
				page.get_full_collection_posts(coll)

				setattr(page, coll, Collection(coll))
				getattr(page, coll).set_posts(page.collections[coll])

				prev_url = page.get_prev_url(start, start + yaml['collections'][coll], coll)
				if prev_url:
					getattr(page, coll).prev_url = request.base_url + prev_url
				next_url = page.get_next_url(start, start - yaml['collections'][coll], coll)
				if next_url:
					getattr(page, coll).next_url = request.base_url + next_url

		del page.collections
