from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_qrcode import QRcode

db = SQLAlchemy()
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///clients.db')

def config_app():
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config['SECRET_KEY'] = 'IEEE'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    db.init_app(app)
    qr_code = QRcode(app)

    # Importing the blueprints
    from .views import views
    from .auth import auth
    from .menu import menu

    # Registering the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(menu, url_prefix='/menu')

    from .models import User

    # Setup for login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.route("/qrcode", methods=["GET"])
    def get_qrcode():
        # please get /qrcode?data=<qrcode_data>
        data = request.args.get("data", "")
        return send_file(qr_code(data, mode="raw"), mimetype="image/png")

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    # Setup for database
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            db.drop_all()
            db.create_all()

    return app