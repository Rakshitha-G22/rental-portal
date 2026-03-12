from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Blueprint, request, jsonify
import os
# from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

# Import blueprints
from .routes.auth import auth_bp
from .routes.bookings import bookings_bp
from .routes.flats import flats_bp
from .routes.admin import admin_bp
from app.routes.user import user_bp

# migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    # migrate.init_app(app, db)
    
    # FIX: Update this to match your live Render Frontend URL
    # CORS will now allow requests from your specific Frontend URL
    allowed_origins = [
        "https://rental-portal-2.onrender.com",
        "http://localhost:4200"]
    
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return '', 200

    # Register blueprints with url_prefix
    # These prefixes match the structure: /api/ + [prefix]
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    app.register_blueprint(flats_bp, url_prefix="/flats")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    
    # user_bp does not have a prefix, ensure its routes include /api if needed
    app.register_blueprint(user_bp)

    @app.route("/api/test-open")
    def test_open():
        return "Backend is running!"
    
    with app.app_context():
        db.create_all() 
    # # This creates all tables from your models automatically

    return app