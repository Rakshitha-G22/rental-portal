from flask import Blueprint, jsonify
from ..models import Flat, Booking
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.models import db, Flat, Booking

flats_bp = Blueprint("flats_bp", __name__)

# ================= GET ALL FLATS =================
@flats_bp.route("/", methods=["GET"])
def get_all_flats():
    try:
        # Load all flats and their associated bookings in one go
        flats = Flat.query.options(joinedload(Flat.bookings)).all()
        flat_list = []

        for flat in flats:
            # Check for any active booking in the loaded relationship
            active_booking = next((b for b in flat.bookings if b.status.lower() in ["confirmed", "pending"]), None)
            
            # ... (your existing amenities logic) ...

            flat_list.append({
                "id": flat.id,
                # ... other fields ...
                "is_booked": active_booking is not None,
                "booking_status": active_booking.status.lower() if active_booking else None
            })

        return jsonify(flat_list), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
        


# ================= GET SINGLE FLAT =================
@flats_bp.route("/<int:flat_id>", methods=["GET"])
def get_flat(flat_id):
    try:
        flat = Flat.query.get(flat_id)

        if not flat:
            return jsonify({"msg": "Flat not found"}), 404

            
        if isinstance(flat.amenities, list):
                amenities_list = flat.amenities
        elif isinstance(flat.amenities, str):
                amenities_list = [a.strip() for a in flat.amenities.split(",")]
        else:
                amenities_list = []

        active_booking = Booking.query.filter(
            Booking.flat_id == flat.id,
            func.lower(Booking.status).in_(["approved", "pending"])
        ).first()

        return jsonify({
            "id": flat.id,
            "flat_number": flat.flat_number,
            "flat_type": flat.flat_type,
            "location": flat.location,
            "price": flat.price,
            "image": flat.image,
            "tower_name": flat.tower_name,
            "floor": flat.floor,
            "amenities": amenities_list,
            "is_booked": active_booking is not None
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


    
@flats_bp.route('/seed-data', methods=['POST'])
def seed_flats():
    sample_flats = [
        Flat(title="Cozy Studio in City Center", price=1200, location="Downtown"),
        Flat(title="Spacious 2-Bedroom Apartment", price=2500, location="Suburbs")
    ]
    
    try:
        db.session.add_all(sample_flats)
        db.session.commit()
        return jsonify({"message": "Database seeded successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

