from app import app
from .views import *

from modules.site import *


def init_admin_data():

	# only for run, not for freeze
	if yasifipo_is_server() == False:
		return False

	# register admin page
	yasifipo_register('/admin/', admin, 'admin', {}, store=False)
	yasifipo_register('/admin/reloading/', reloading, 'reloading', {}, ['POST'], store=False)
