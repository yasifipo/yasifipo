# Yasifipo

Yet Another Simple File Posting Organizer
Still in heavy development. Do not use in production for now
Yasifipo is running using python & Flask
No database, using only filesystem

# Features
*  Multisite
*  Multilanguage

# Modules
*  prez, generate complete courses (including Table of content) presentations using reveal.js
*  pages, generate pages website
*  blog, generate blog posts

# how to run
*  python app/manage.py run -d path/to/data/
*  python app/manage.py freeze -d path/to/data/

# Docs
List of all existing yaml files

## _data/prez/summary.md
Contains list of all available prez (table of __prez__ in yaml)
*  directory: mandatory, must be path to presentation (in filesystem), without any slash
*  lang: optional, lang of prez. default_lang will be used if not set
*  draft: optional, html files are not generated if set to True
*  (any tag): optional
*  server: optional, can be a str or list: server (or list of server) where presentation will be published
*  single: optional. If set, is name of single file in directory. No TOC in this case, only 1 prez is available
*  static: optional. Will register all files inside as static files (works only for single-prez)
*  content (not part of yaml): not taken into account
*  tags: optional. If set to False, tags are not displayed

## .chapter in any path of prez
Create your table of content by creating a directory tree. Each path must have a .chapter.md file, or it will be created automatically:  
*  slug: mandatory, url part of the current chapter (can be '' for displaying at url root)
*  title: mandatory, title of chapter
*  draft: optional, will not be taken into account if set to True
*  display-toc: optional, will not display ToC if set to False
*  cucumber: optional, will not display cucumber if set to False
*  ref: optional (except if category is set), used to identify prez regarding language (same prez in 2 different languages must have same _ref_ field)
*  (any tag): optional
*  static: mandatory, name of folder that can contains files like images
*  tags: optional. If set to False, tags are not displayed
*  content (not part of yaml): will be displayed in chapter page
*  redirect (str or tab) : urls redirected to url by 301 redirection
*  layout: optional. Set the layout (in templates/prez folder). If not set, default is used

## any prez file
*  slug: mandatory, url part of the current presentation
*  title: mandatory, title of presentation
*  draft: optional, will not be taken into account if set to True
*  cucumber: optional, will not display cucumber if set to False, never displayed for single prez
*  ref: optional (except if category is set), used to identify prez regarding language (same prez in 2 different languages must have same _ref_ field)
*  (any tag): optional
*  content (not part of yaml): content of reveal.js presentation. By default:
  *  ~~~ is used for horizontal separator
  *  ~~ is used for vertical separator
*  theme:(optional) use a specific reveal.js theme. If not set, will use global config reveal_default_theme
*  redirect (str or tab) : urls redirected to url by 301 redirection
*  page: optional, prez is displayed as a page, not with reveal presentation mode
*  tags: optional. If set to False, tags are not displayed
*  layout: optional. Set the layout (in templates/prez folder). If not set, default is used

## page file
*  url: mandatory, url of page
*  title: mandatory, title of page
*  lang: optionnal, lang of page. default_lang will be used if not set
*  ref: optional (but mandatory if to display cucumber), used to identify pages regarding language (same page in 2 different languages must have same _ref_ field)
*  parent: optional, ref of parent page (for cucumber display)
*  cucumber: optional, will not display cucumber if set to False
*  server: optional, can be a str or list: server (or list of server) where page will be published
*  (any tag): optional
*  content (not part of yaml): content of page (in markdown language)
*  tags: optional. If set to False, tags are not displayed
*  redirect (str or tab) : urls redirected to url by 301 redirection
*  layout: optional. Set the layout (in templates/page folder). If not set, default is used
*  posts: optional. If set to True, all posts are retrieved and available in page.posts ; If set to an INT, pagination is setup with split every number set in this value
