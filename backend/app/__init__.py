# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os  # your config file

# Initialize extensions (without app)
db = SQLAlchemy()
jwt = JWTManager()

# Import blueprints from routes
from .routes.auth import auth_bp
from .routes.bookings import bookings_bp
from .routes.flats import flats_bp
from .routes.admin import admin_bp
from app.routes.user import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    allowed_origin = os.environ.get('FRONTEND_URL', 'http://localhost:4200')

    CORS(app, resources={r"/api/*": {"origins": allowed_origin}})

    # Register blueprints with url_prefix
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")
    app.register_blueprint(flats_bp, url_prefix="/api")
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Optional: a simple test route
    @app.route("/api/test-open")
    def test_open():
        return "Backend is running!"

    return app