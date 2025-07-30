import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    
    RELATIVE_UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads")
    UPLOAD_FOLDER = os.path.join(basedir, 'app', RELATIVE_UPLOAD_FOLDER)
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///portfolio.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")