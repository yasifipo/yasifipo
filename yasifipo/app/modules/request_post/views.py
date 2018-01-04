from app import app
from flask import render_template

def render_request_post(file_, post, request):
    if hasattr(app.post, post):
        if callable(getattr(app.post, post)):
            return getattr(app.post, post)(file_, request)
        else:
            return getattr(app.post, "default_post")(file_, request)
    else:
        return getattr(app.post, "default_post")(file_, request)


def default_post(file_, request):
    return render_template('site/default_request_post.html')
