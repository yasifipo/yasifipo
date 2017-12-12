from shutil import copytree


def init_yasifipo_minimal(directory):
	print("Creating minimal data directory...")
	copytree("app/modules/init/_data_minimal", directory)
