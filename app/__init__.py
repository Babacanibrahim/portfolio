from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Modelleri içe aktar
    from app import models

    # Rotaları kaydet
    from app.routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    return app
