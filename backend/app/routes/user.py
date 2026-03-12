# app/routes/user.py

from flask import Blueprint, request, jsonify, make_response
from app.models import User, Flat, Booking, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


# =============================
# REGISTER
# =============================

@user_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        name=data.get('name', '')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# =============================
# LOGIN
# =============================

@user_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):

        return jsonify({
            "message": "Login successful",
            "email": user.email,
            "name": user.name,
            "is_admin": user.role == "admin"
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401


# =============================
# GET ALL FLATS (FOR USERS)
# =============================

@user_bp.route('/flats', methods=['GET'])
def get_flats():

    flats = Flat.query.all()

    result = []

    for f in flats:

        result.append({
            "id": f.id,
            "flat_number": f.flat_number,
            "flat_type": f.flat_type,
            "tower_name": f.tower_name,
            "location": f.location,
            "floor": f.floor,
            "price": f.price,
            "image": f.image,
            "is_booked": f.is_booked,
            "amenities": f.amenities if isinstance(f.amenities, list) else []
        })

    response = make_response(jsonify(result), 200)
    response.headers["Cache-Control"] = "no-store"

    return response


# =============================
# BOOK A FLAT
# =============================

@user_bp.route('/book', methods=['POST'])
def book_flat():

    data = request.get_json()

    email = data.get("email")
    flat_id = data.get("flat_id")

    if not email or not flat_id:
        return jsonify({"error": "Email and flat_id required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    flat = Flat.query.get(flat_id)

    if not flat:
        return jsonify({"error": "Flat not found"}), 404

    # Check if flat already booked
    if flat.is_booked:
        return jsonify({"error": "Flat already booked"}), 400

    # Check if user already requested booking
    existing_booking = Booking.query.filter_by(
        user_id=user.id,
        flat_id=flat.id
    ).first()

    if existing_booking:
        return jsonify({"error": "You already requested this flat"}), 400

    booking = Booking(
        user_id=user.id,
        flat_id=flat.id,
        status="pending",
        booked_at=datetime.utcnow()
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Booking request sent",
        "booking_id": booking.id
    }), 201


# =============================
# VIEW USER BOOKINGS
# =============================

@user_bp.route('/bookings/<email>', methods=['GET'])
def get_bookings(email):

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    bookings = Booking.query.filter_by(user_id=user.id).all()

    result = []

    for b in bookings:

        result.append({
            "id": b.id,
            "flat_number": b.flat.flat_number,
            "flat_type": b.flat.flat_type,
            "tower_name": b.flat.tower_name,
            "location": b.flat.location,
            "status": b.status,
            "booked_at": b.booked_at.strftime("%Y-%m-%d %H:%M:%S") if b.booked_at else None
        })

    response = make_response(jsonify(result), 200)
    response.headers["Cache-Control"] = "no-store"

    return response