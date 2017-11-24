from flask import render_template, redirect, url_for

from .helpers import *


def admin():
	return render_template('admin/admin.html')

def reloading():
	reloading_data()
	return redirect(url_for('admin'))
