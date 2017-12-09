from app import app

import sys

from flask import url_for
from flask_frozen import relative_url_for

def yasifipo_is_server():
	if len(sys.argv) >= 2 and sys.argv[1] == "freeze":
		return False
	else:
		return True

def yasifipo_url_for(target, **values):
	if yasifipo_is_server() == False:
		return relative_url_for(target, **values)
	else:
		return url_for(target, **values)
