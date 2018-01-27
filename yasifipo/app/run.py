from app import app

from modules.site import *
from main import *

load_config()
templates_add_loader(app.config['TEMPLATES_DIR']) #must be before Plugin registration
run_data_read(app)

if 'yasifipo_subdirectory' in app.yasifipo['config'] and app.yasifipo['config']['yasifipo_subdirectory'] != '':
    app.register_blueprint(admin, url_prefix="/" + app.yasifipo['config']['yasifipo_subdirectory'] + "/admin")
else:
    app.register_blueprint(admin, url_prefix="/admin")


if __name__ == "__main__":
    app.run()
