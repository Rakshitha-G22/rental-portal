import os
from flask_migrate import Migrate
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import logging


db = SQLAlchemy()
jwt = JWTManager()



def create_app():

    app = Flask(__name__, static_folder=ANGULAR_DIST)
    logging.basicConfig(level=logging.DEBUG)

    # ==========================
    # CONFIG
    # ==========================
    app.config.from_object("config.Config")

    # ==========================
    # JWT CONFIG
    # ==========================
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "rental-portal-super-secure-jwt-secret-key"
    )
#     app.config["JWT_SECRET_KEY"] = os.getenv(
#     "JWT_SECRET_KEY",
#     "dev-secret-key-change-in-production"
# )

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)

    # ==========================
    # DATABASE CONFIG
    # ==========================
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        db_url = "postgresql://postgres:Rakshu%40123@localhost:5432/rental-portal"

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ==========================
    # EXTENSIONS
    # ==========================
    db.init_app(app)
    jwt.init_app(app)

    Migrate(app, db)

    # ==========================
    # CORS CONFIG
    # ==========================
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:4200",
                    "https://perpetual-miracle-production-e3d3.up.railway.app"
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        }
    )


    @app.before_request
    def handle_options_request():
        if request.method == "OPTIONS":
            response = jsonify({})
            response.status_code = 200
            return response
    # ⭐ AFTER REQUEST HEADERS
    @app.after_request
    def add_headers(response):
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    # Catch API routing properly
    @app.errorhandler(404)
    def api_not_found(e):
        return jsonify({"msg": "API not found"}), 404
    
    @app.route("/api/test")
    def test():
        return {"message": "Backend working"}

    # ==========================
    # IMPORT ROUTES
    # ==========================
    from .routes.auth import auth_bp
    from .routes.flats import flats_bp
    from .routes.admin import admin_bp
    from .routes.bookings import bookings_bp

    # ==========================
    # REGISTER BLUEPRINTS
    # ==========================
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(flats_bp)
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")


    # ==========================
# SERVE ANGULAR FRONTEND
# ==========================
# Path to Angular build
# ==========================
# SERVE ANGULAR FRONTEND
# ==========================
# Path to Angular build
    ANGULAR_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend/user-app/dist/user-app/browser")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_angular(path):
        """
        Serve Angular SPA:
        - If requested file exists (JS/CSS/etc), serve it.
        - Otherwise serve index.html (Angular handles routing).
        """
        file_path = os.path.join(ANGULAR_DIST, path)  # must be inside function
        if path != "" and os.path.exists(file_path):
        # Serve static file
            return app.send_static_file(path)
        else:
        # Serve Angular index.html for all other routes
            return app.send_static_file("index.html")

    return app