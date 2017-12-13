import os

class Configuration(object):
	DEBUG = True
	SECRET_KEY = 'secret key here!!!'
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))

	YASIFIPO_SERVER = 'test.julienduroure.com'

	DATA_DIR = APPLICATION_DIR + '/_data/' # / before and after

	PREZ_URL_PREFIX = '' # 'slug' without any /
	POST_URL_PREFIX = '' # 'slug' without any /

	FREEZER_RELATIVE_URLS = True

	DEFAULT_LANG = 'en'
	REVEAL_DEFAULT_THEME = "yasifipo"
