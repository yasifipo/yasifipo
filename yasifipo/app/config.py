import os

class Configuration(object):
	DEBUG = True
	SECRET_KEY = 'secret key here!!!'
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))

	#TODO put to yasifipo config file
	YASIFIPO_SERVER = 'test.julienduroure.com'

	DATA_DIR = APPLICATION_DIR + '/_data/' # / before and after

	CONFIG_DIR = DATA_DIR + "config/" # / after
	LANGS_DIR  = DATA_DIR + "langs/" # / after
	PREZ_DIR   = DATA_DIR + 'prez/' # / after
	PAGE_DIR   = DATA_DIR + "pages/" # / after
	CAT_DIR    = DATA_DIR + "categories/" # / after

	PREZ_URL_PREFIX = '' # 'slug' without any /

	FREEZER_RELATIVE_URLS = True

	DEFAULT_LANG = 'en'
	REVEAL_DEFAULT_THEME = "beige"
