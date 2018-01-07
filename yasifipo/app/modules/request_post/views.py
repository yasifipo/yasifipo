from app import app
from flask import render_template

def render_request_post(file_, post, request):
	if '/' in post:
		# Coming from a plugin
		plugin_value, post_value = post.split('/')
		if plugin_value not in app.plugins.keys():
			return getattr(app.post, "default_post")(file_, request)
		if not callable(getattr(app.plugins[plugin_value], post_value)):
			return getattr(app.post, "default_post")(file_, request)
		return getattr(app.plugins[plugin_value], post_value)(file_, request)

	# Coming from core yasifipo
	else:
		if hasattr(app.post, post):
			if callable(getattr(app.post, post)):
				return getattr(app.post, post)(file_, request)
			else:
				return getattr(app.post, "default_post")(file_, request)
		else:
			return getattr(app.post, "default_post")(file_, request)


def default_post(file_, request):
	return render_template('site/default_request_post.html')
