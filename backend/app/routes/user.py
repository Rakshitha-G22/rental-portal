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
            "is_admin": user.is_admin
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401

# =============================
# GET ALL FLATS
# =============================
@user_bp.route('/flats', methods=['GET'])
def get_flats():
    flats = Flat.query.all()
    data = [
        {
            "id": f.id,
            "title": f"{f.tower} {f.number}",
            "tower": f.tower,
            "number": f.number,
            "size": f.size,
            "amenities": f.amenities.split(', ') if f.amenities else []
        } for f in flats
    ]
    response = make_response(jsonify(data), 200)
    response.headers["Cache-Control"] = "no-store"  # prevent 304 caching issues
    return response

# =============================
# BOOK A FLAT
# =============================
@user_bp.route('/book', methods=['POST'])
def book_flat():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    flat = Flat.query.get(data.get('flat_id'))
    if not flat:
        return jsonify({"error": "Flat not found"}), 404

    # Optional: check if already booked
    if Booking.query.filter_by(flat_id=flat.id, status='confirmed').first():
        return jsonify({"error": "Flat already booked"}), 400

    booking = Booking(user_id=user.id, flat_id=flat.id, status='pending', booked_on=datetime.utcnow())
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking requested successfully", "booking_id": booking.id}), 201

# =============================
# VIEW BOOKINGS
# =============================
@user_bp.route('/bookings/<email>', methods=['GET'])
def get_bookings(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    bookings = [
        {
            "id": b.id,
            "flat_title": f"{b.flat.tower} {b.flat.number}",
            "status": b.status,
            "booked_on": b.booked_on.strftime("%Y-%m-%d %H:%M:%S") if b.booked_on else None
        } for b in user.bookings
    ]
    response = make_response(jsonify(bookings), 200)
    response.headers["Cache-Control"] = "no-store"
    return response