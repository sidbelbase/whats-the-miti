from flask import Flask
from flask_cors import CORS
from .config import Configuration

cors = CORS()


def create_app(config_class=Configuration):
    app = Flask(__name__)
    cors.init_app(app)
    app.config.from_object(Configuration)

    from whatsthemiti.api.routes import api
    from whatsthemiti.main.routes import main

    app.register_blueprint(api)
    app.register_blueprint(main)
    return app
