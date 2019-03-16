from app import app
from modules.site import *
from datetime import datetime
from frontmatter import load
from modules.utils.date import *
import os

def importing_post(ext, data):

    for lang in data:

        # Do not import post that are not in a known lang here
        if lang not in [lg['lang'] for lg in app.yasifipo['langs'].values()]:
            continue

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


def importing_own_post(ext):

    # retrieve tag type of the tag
    tag_type = None
    for type_ in app.yasifipo["tags"]["data"].keys():
        for tag in app.yasifipo["tags"]["data"][type_].keys():
            if tag == ext['tag']:
                tag_type = type_
                break
        if tag_type is not None:
            break

    for lang in app.yasifipo["tags"]["data"][tag_type][ext['tag']]['data'].keys():
        for post in app.yasifipo["tags"]["data"][tag_type][ext['tag']]['data'][lang].values():
            if post['type'] == "post":

                title = ""
                with open(post['file']) as f:
                    yaml = load(f)
                    title = yaml['title']
                    date, in_yaml, in_file = get_date(yaml, os.path.basename(post['file']))
                    if in_yaml is False and in_file is False:
                        continue

                    app.yasifipo['externals']['data']["posts"][lang].append({
                        'file':  None,
                        'title': title,
                        'lang': lang,
                        'date': date,
                        'url': yasifipo_url_for('render_file', path=app.yasifipo["files"][post['file']]),
                        'ext': ext['slug'],
                        'prev': None,
                        'next': None
                    })

def importing_post_after():
	for lang in app.yasifipo['externals']['data']["posts"] .keys():
		app.yasifipo['externals']['data']["posts"] [lang] = sorted(app.yasifipo['externals']['data']["posts"][lang], key=lambda k: k['date'])
		app.yasifipo['externals']['data']["posts"] [lang].reverse()
