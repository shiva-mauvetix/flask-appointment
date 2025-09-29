import logging

from flask import Flask

from .config import Config
from .extensions import cors, db, migrate
from .routes import api


def create_app():
    app = Flask(import_name=__name__)
    app.config.from_object(Config)

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(filename="app.log"), logging.StreamHandler()],
    )

    # Init extensions
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    # app factory
    cors.init_app(
        app=app,
        # origins=[
        #     "http://localhost:3000",
        #     "https://slateblue-oyster-554718.hostingersite.com",
        #     "https://appointments.socialvave.in/",
        # ],
        origins="*",
        methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=[
            "Content-Type",
            "Authorization",
        ],
        supports_credentials=True,
    )

    app.register_blueprint(blueprint=api)

    return app

