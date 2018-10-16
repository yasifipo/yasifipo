import shutil
import os

def yasifipo_copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def init_yasifipo_minimal(directory):
	print("Creating minimal data directory...")
	shutil.copytree("app/modules/init/_data_minimal", directory)

	# copy templates
	yasifipo_copytree("app/templates/default", directory + "/templates/default/")

	# copy css + js
	yasifipo_copytree("app/static", directory + "/static/")
