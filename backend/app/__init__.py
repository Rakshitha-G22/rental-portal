# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config  # your config file

# Initialize extensions (without app)
db = SQLAlchemy()
jwt = JWTManager()

# Import blueprints from routes
from .routes.auth import auth_bp
from .routes.booking import booking_bp
from .routes.flats import flats_bp
from .routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # enable CORS for all routes

    # Register blueprints with url_prefix
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(booking_bp, url_prefix="/api/booking")
    app.register_blueprint(flats_bp, url_prefix="/api/flats")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Optional: a simple test route
    @app.route("/api/test-open")
    def test_open():
        return "Backend is running!"

    return app