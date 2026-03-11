from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Your config file
    CORS(app)  # Enable CORS globally

    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from .auth import auth_bp
    from .booking import booking_bp
    from .flats import flats_bp
    from .admin import admin_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(booking_bp, url_prefix="/api/booking")
    app.register_blueprint(flats_bp, url_prefix="/api/flats")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Test endpoint
    @app.route("/api/test-open")
    def test_open():
        return {"message": "Backend is running!"}

    return app