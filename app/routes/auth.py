from flask import Blueprint, request, jsonify
from .. import db
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth_bp", __name__)


# ------------------------
# REGISTER USER
# ------------------------
@auth_bp.route("/register", methods=["POST", "OPTIONS"])
def register():

    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not name or not email or not password:
            return jsonify({"msg": "All fields required"}), 400

        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "User already exists"}), 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# ------------------------
# LOGIN USER
# ------------------------
@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():

    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json()

        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid credentials"}), 401

        # Create JWT token
        access_token = create_access_token(
            identity=str(user.id)
        )

        return jsonify({
            "access_token": access_token,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "msg": "Login successful"
        }), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500