
from modules.site import *

from modules.site.langs import *

from flask import render_template
from flask import Markup
from markdown import markdown

from .helpers import *

def display_page(file_):
    with open(file_) as data:
        yaml = load(data)

        if 'ref' in yaml.keys():
            langs = get_langs_from_ref('display_page', yaml['ref'])

        #cucumber
        cucumber = []
        if 'cucumber' not in yaml.keys() or ('cucumber' in yaml.keys() and yaml['cucumber'] != False):
            if 'ref' in yaml.keys() and 'parent' in yaml.keys():
                if 'lang' not in yaml.keys():
                    lang = app.config['DEFAULT_LANG']
                else:
                    lang = yaml['lang']
                cucumber = get_page_cucumber(yaml['ref'], lang)

        category = {}
        if 'lang' in yaml.keys():
            lang = yaml['lang']
        else:
            lang = app.config['DEFAULT_LANG']
        if 'category' in yaml.keys():
            category['descr'] = app.yasifipo['categories'][yaml['category']][lang]['descr']
            category['url']   = yasifipo_url_for('display_category', category=yaml['category'], lang=lang)

        return render_template('page/page.html', title=yaml['title'], content=Markup(markdown(yaml.content)), cucumber=cucumber, langs=langs, category=category)
