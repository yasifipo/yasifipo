from app import app
from flask import render_template

def render_redirection(url):
	return render_template('site/redirect.html', link=url)
