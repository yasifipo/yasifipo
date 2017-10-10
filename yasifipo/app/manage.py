from app import manager
from main import app
from flask_frozen import Freezer

freezer = Freezer(app)

@freezer.register_generator
def url_generator():
	for i in app.yasifipo['frozen']:
		yield i[0], i[1]

@manager.command
def freeze():
	freezer.freeze()

if __name__ == '__main__':
	manager.run()
