from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .. import db
from ..models import User

auth_bp = Blueprint("auth_bp", __name__)

# =============================
# REGISTER
# =============================
@auth_bp.route("/register", methods=["POST"]) # REMOVE "OPTIONS" here
def register():
    # flask-cors handles OPTIONS automatically, so we remove the manual check
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"msg": "All fields required"}), 400

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

    return jsonify({"msg": "Registration successful"}), 201

# =============================
# LOGIN
# =============================
@auth_bp.route("/login", methods=["POST"]) # REMOVE "OPTIONS" here
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"msg": "All fields required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid credentials"}), 401

        # Identity must be a string for JWT
        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "name": user.name,
            "role": user.role,
            "msg": "Login successful"
        }), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500