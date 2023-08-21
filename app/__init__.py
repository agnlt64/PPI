from flask import Flask
import secrets

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_urlsafe(40)

    from .views import views
    app.register_blueprint(views)

    return app