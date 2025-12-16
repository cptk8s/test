from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from . import models
    from .routes import api_bp

    app.register_blueprint(api_bp)

    @app.errorhandler(ValidationError)
    def handle_marshmallow(err):
        return {'errors': err.messages}, 400

    with app.app_context():
        db.create_all()

    return app
