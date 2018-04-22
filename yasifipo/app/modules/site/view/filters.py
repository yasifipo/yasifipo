import re
from frontmatter import load
from app import app
from flask import render_template

from os.path import dirname, join

@app.template_filter()
def gmarkdown(text):
	return Markup(markdown(text, app.yasifipo["markdown_process"]))

@app.template_filter()
def youtube(text):
	return render_template('includes/filters/youtube.html', id=text)

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