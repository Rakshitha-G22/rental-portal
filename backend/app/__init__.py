import os
import logging
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

# ==========================================
# PATH TO ANGULAR STATIC FILES
# ==========================================
basedir = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(basedir, "..", "frontend", "user-app", "dist", "user-app", "browser")

def create_app():
    # Flask app with Angular static folder
    app = Flask(__name__, static_folder=static_dir, static_url_path="")
    logging.basicConfig(level=logging.DEBUG)

    # ==========================
    # CORS CONFIGURATION
    # ==========================
    allowed_origins = [
        "http://localhost:4200",
        "https://perpetual-miracle-production-e3d3.up.railway.app"
    ]

    CORS(
        app, 
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # ==========================
    # APP CONFIG
    # ==========================
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "rental-portal-super-secure-jwt-secret-key"
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)

    db_url = os.getenv("DATABASE_URL") or "postgresql://postgres:Rakshu%40123@localhost:5432/rental-portal"
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ==========================
    # INITIALIZE EXTENSIONS
    # ==========================
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # ==========================
    # REGISTER BLUEPRINTS
    # ==========================
    from .routes.auth import auth_bp
    from .routes.flats import flats_bp
    from .routes.admin import admin_bp
    from .routes.bookings import bookings_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(flats_bp)
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")

    # ==========================
    # TEST API
    # ==========================
    @app.route("/api/test")
    def test():
        return jsonify({"message": "Backend working", "status": "success"})

    # ==========================
    # SERVE ANGULAR FRONTEND
    # ==========================
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_angular(path):
        # Serve requested static file if exists
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return app.send_static_file(path)
        # Otherwise serve index.html for Angular routing
        return app.send_static_file("index.html")

    return app