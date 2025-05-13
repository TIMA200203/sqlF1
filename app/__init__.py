from flask import Flask
from app.models import db
from app.api import api_bp
from settings import settings


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
