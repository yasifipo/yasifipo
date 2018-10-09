---
yasifipo_server: example.yasifipo.net
yasifipo_resource_server: ['example-resource.yasifipo.net', 'example2-resource.yasifipo.net']
yasifipo_subdirectory: '' # without any /, or '' for using root

prez_url_prefix: '' # 'slug' without any /
post_url_prefix: '' # 'slug' without any /
post_default_url: <lang>/<year>/<month>/ # with / at end, but without / at beginning
collection_default_url: <lang>/<year>/<month>/ # with / at end, but without / at beginning

default_lang: 'en'
theme: 'default'

reveal_default_theme: "yasifipo"

layout_page: 'page/page.html'
layout_post: 'post/post.html'
layout_prez: 'prez/prez.html'
layout_chapter: 'prez/toc.html'
layout_prez_page: 'prez/page.html'
layout_collection: 'collection/collection.html'

site_version: 0.0.1
dont_freeze: False
freeze_dir: build
freeze_destination_ignore: []
---
