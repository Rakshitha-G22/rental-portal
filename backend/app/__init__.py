import os
import logging
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

# Path to your frontend src
basedir = os.path.abspath(os.path.dirname(__file__))
# We add "browser" at the end because that's where index.html is
static_dir = os.path.join(basedir, "..", "frontend", "user-app", "dist", "user-app", "browser")
app = Flask(__name__, static_folder=static_dir, static_url_path="")

def create_app():
    logging.basicConfig(level=logging.DEBUG)

    # ========================== CORS ==========================
    allowed_origins = [
        "http://localhost:4200",
        "https://perpetual-miracle-production-e3d3.up.railway.app"
    ]
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

    # ========================== JWT ==========================
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "rental-portal-super-secure-jwt-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)

    # ========================== DATABASE ==========================
    db_url = os.getenv("DATABASE_URL") or "postgresql://postgres:Rakshu%40123@localhost:5432/rental-portal"
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # ========================== BLUEPRINTS ==========================
    from .routes.auth import auth_bp
    from .routes.flats import flats_bp
    from .routes.admin import admin_bp
    from .routes.bookings import bookings_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(flats_bp)
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")

    @app.route("/api/test-open")
    def test_open():
        return jsonify({"message": "Backend working without login", "status": "success"})

    @app.route("/")
    def hello():
        return "Hello World! Backend is running locally."
    
    
    @app.route("/api/test-open")
    def test_open():
        
        return jsonify({"message": "Backend working without login", "status": "success"})
    @app.route("/api/test")
    def test():
        return jsonify({"message": "Backend working", "status": "success"})

    # ========================== SERVE INDEX.HTML ==========================
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_angular(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return app.send_static_file(path)
        return app.send_static_file("index.html")

    return app