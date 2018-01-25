import os

class Configuration(object):
	DEBUG = True

	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))

	DATA_DIR = APPLICATION_DIR + '/_data/' # / before and after

	FREEZER_RELATIVE_URLS = True
	FREEZER_DESTINATION = 'build'

	VERSION = "0.0.1"

	DISPLAY_ALL = False
