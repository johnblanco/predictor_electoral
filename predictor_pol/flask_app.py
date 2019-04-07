# para correr: export FLASK_APP=flask_app.py;flask run
import logging

from flask import Flask, g

import db_manager
from views import aquienvoto

BLUEPRINTS = (aquienvoto.bp,)
logger = logging.getLogger("aquienvotoUY")


def create_app(config=None):
    app = Flask(__name__, template_folder="templates")
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    configure_logging(app)
    configure_blueprints(app, BLUEPRINTS)

    return app


def configure_logging(app):
    # Log to standard output/error
    logging.basicConfig(
        format="%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=logging.INFO,
    )


def configure_blueprints(app, blueprints):
    logger.info(f"Registering blueprints = {', '.join([bp.name for bp in blueprints])}")
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


app = create_app()


@app.teardown_appcontext
def close_connection(exception):
    db_manager.close_connection()
