from app import app
from modules.site import *
from datetime import datetime

def importing_post(ext, data):

    for lang in data:

        lang = set_lang({'lang':lang})

        for post in data[lang]:
            # No need to have ref, because this is only links to other website
            # TODO manage tags
            # TODO manage tag linked to external repo
            date =  datetime.strptime(str(post['date']), "%Y-%m-%d")
            url = post['url']

            if lang not in app.yasifipo['externals']['data']["posts"].keys():
                app.yasifipo['externals']['data']["posts"] [lang] = []

            app.yasifipo['externals']['data']["posts"][lang].append({
    			'file': None,
                'title': post['title'],
    			'lang': lang,
    			'date': date,
    			'url': url,
                'ext': ext,
                'prev': None,
                'next': None
    			})

def importing_post_after():
	for lang in app.yasifipo['externals']['data']["posts"] .keys():
		app.yasifipo['externals']['data']["posts"] [lang] = sorted(app.yasifipo['externals']['data']["posts"][lang], key=lambda k: k['date'])
		app.yasifipo['externals']['data']["posts"] [lang].reverse()
