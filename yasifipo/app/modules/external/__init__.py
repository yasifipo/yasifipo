from app import app
from modules.post.export import *
from modules.post.importing import *
import json
from os.path import isfile
from frontmatter import load


def init_external_data():
    if isfile(app.config['CONFIG_DIR'] + "externals.md"):
        with open(app.config['CONFIG_DIR'] + "externals.md", "r") as f:
            yaml = load(f)
            for ext in yaml['externals']:
                app.yasifipo['externals']['conf'][ext['slug']] = ext

    app.yasifipo['externals']['data'] = {}
    app.yasifipo['externals']['data']["posts"] = {}
    for ext in app.yasifipo['externals']['conf'].values():

        if "self" in ext.keys() and type(ext['self']).__name__ == "bool" and ext['self'] == True:
            continue

        if not isfile(ext['path']):
            print("ERROR external file not found " + ext['path'])
            continue

        with open(ext['path'], "r") as f:
            json_ = json.loads(f.read())

            if 'posts' in json_.keys():
                importing_post(ext['slug'], json_['posts'])


    # Importing own posts into external
    for ext in app.yasifipo['externals']['conf'].values():
        if not ("self" in ext.keys() and type(ext['self']).__name__ == "bool" and ext['self'] == True):
            continue

        importing_own_post(ext)


    # After reading all externals site
    if "posts" in app.yasifipo["externals"]["data"].keys():
        importing_post_after()

def export_all(output):
    app.exporter = {}
    app.exporter["posts"] = {}
    export_post()

    with open(output, "w") as f:
        json.dump(app.exporter, f)
