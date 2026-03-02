from flask import Flask
from todo.views.routes import api, reset_store


def create_app() -> Flask:
    app = Flask(__name__)

    # important: reset in-memory store for each new app/test run
    reset_store()

    app.register_blueprint(api)
    return app