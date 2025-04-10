from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and login manager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# IMPORTANT: Import routes so that routes are registeredss
from routes import *

# Create the database tables if they do not exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
