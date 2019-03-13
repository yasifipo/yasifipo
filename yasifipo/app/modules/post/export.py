from app import app
from modules.site.view.urls import *
from frontmatter import load

def export_post():

    for lang in app.yasifipo["posts"]:

        if lang not in app.exporter["posts"].keys():
            app.exporter["posts"][lang] = []

        for post in app.yasifipo["posts"][lang]:
            post_ = {}
            if post["resource"] is not None:
                continue

            # TODO manage http / https
            post_['url'] = 'http://' + app.yasifipo['config']['yasifipo_server'] + yasifipo_url_for('render_file', path=app.yasifipo["files"][post["file"]])
            post_['lang'] = lang
            if 'ref' in post.keys():
                post_['ref'] = post['ref']
            post_['date'] = str(post['date'])[:10]

            # open file to get title
            with open(post["file"], encoding='utf-8') as data:
                yaml = load(data)
                post_['title'] = yaml['title']

            app.exporter["posts"][lang].append(post_)
