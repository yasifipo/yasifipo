import re
from frontmatter import load
from app import app
from flask import render_template
from flask import Markup

from os.path import dirname, join
from .urls import *

@app.template_filter()
def gmarkdown(text):
	return Markup(markdown(text, extensions=app.yasifipo["markdown_process"]))

@app.template_filter()
def yasifipo(text):
	return yasifipo_url_for('render_file', path=app.yasifipo["files"][app.config['DATA_DIR'] + text])

@app.template_filter()
def static(text):
	return yasifipo_url_for('static', filename=text)

@app.template_filter()
def youtube(text):
	return render_template('includes/filters/youtube.html', id=text)

@app.template_filter()
def onlydate(text):
	return str(text)[:10]

@app.template_filter()
def include(text):
	with open(text) as fil_include:
		yaml_include = load(fil_include)

		return yaml_include.content


def pre_filter_abs_path(current_file, file):
	return join(dirname(current_file), file)

def pre_filter(data, text):
	matches = re.findall(r"\{\{( *)(\"|\'{1})(?P<file>.*?)(\"|\'{1})( *)\|( *)include( *)\}\}", text)
	if matches is None:
		return text

	for m in matches:
		text = text.replace(m[2], pre_filter_abs_path(data['file'], m[2]))

	return text
