from app import app
from flask import render_template

@app.template_filter()
def gmarkdown(text):
	return Markup(markdown(text, app.yasifipo["markdown_process"]))

@app.template_filter()
def youtube(text):
	return render_template('includes/filters/youtube.html', id=text)
