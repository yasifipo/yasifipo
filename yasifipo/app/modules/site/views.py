from flask import send_from_directory

def return_file(path_, file_):
	return send_from_directory(path_, file_)
