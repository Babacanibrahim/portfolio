from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
import os
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # <-- burada tanımla

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # <-- burada başlat

    # Modelleri içe aktar
    from app import models

    # Rotaları kaydet
    from app.routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()  # bu kalsın, migrate ile çakışmaz

    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    return app

