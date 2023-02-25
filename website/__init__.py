from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "clients.db"

def config_app():
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config['SECRET_KEY'] = 'IEEE'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    
    # Registering the blueprint
    app.register_blueprint(views, url_prefix='/')
    
    # Setup for database
    with app.app_context():
        db.create_all()
    
    return app