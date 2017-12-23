from flask_login import UserMixin
from frontmatter import load
from app import login_manager

@login_manager.user_loader
def load_user(id):
    return User()

class User(UserMixin):

	def __init__(self):
		pass

	def get_id(self):
		return 'admin'

def get_password_hash():
	with open('app/pass.md') as file_:
		yaml = load(file_)

		return yaml['pass']
