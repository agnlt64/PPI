from flask import Flask
from PyLog.logger import Logger
import secrets

client_logger = Logger()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(40)

    from .views import views
    app.register_blueprint(views)

    return app