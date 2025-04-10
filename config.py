import os


basedir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.join(basedir, 'data')


class Config:
    SECRET_KEY = 'your-secret-key'  # Change this to a strong secret key
    DB_FILE = os.path.join(BASE_DIR, "app.db")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
