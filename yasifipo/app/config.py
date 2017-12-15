import os

class Configuration(object):
	DEBUG = True
	SECRET_KEY = 'secret key here!!!'
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))

	DATA_DIR = APPLICATION_DIR + '/_data/' # / before and after

	FREEZER_RELATIVE_URLS = True
