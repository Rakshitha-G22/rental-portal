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
        # Eager load bookings to check availability
        flats = Flat.query.options(joinedload(Flat.bookings)).all()
        flat_list = []

        for flat in flats:
            # Safely check for active booking
            active_booking = None
            if flat.bookings:
                active_booking = next(
                    (b for b in flat.bookings if b.status and b.status.lower() in ["confirmed", "pending"]), 
                    None
                )
            
            flat_list.append({
                "id": flat.id,
                "flat_number": flat.flat_number,
                "flat_type": flat.flat_type,
                "location": flat.location,
                "price": flat.price,
                "image": flat.image,
                "tower_name": flat.tower_name,
                "floor": flat.floor,
                "amenities": flat.amenities,
                "is_booked": active_booking is not None,
                # Use .get() or ternary to prevent errors if status is None
                "booking_status": active_booking.status.lower() if active_booking and active_booking.status else None
            })

        return jsonify(flat_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
        Flat(
            flat_number="101-A",
            flat_type="Studio",
            location="Downtown Manhattan",
            price=1200.0,
            tower_name="Alpha",
            floor=1,
            image="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267",
            amenities=["WiFi", "Air Conditioning", "Kitchenette"],
            is_booked=False
        ),
        Flat(
            flat_number="502-B",
            flat_type="2-Bedroom",
            location="Brooklyn Heights",
            price=2800.0,
            tower_name="Bravo",
            floor=5,
            image="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
            amenities=["Balcony", "Gym Access", "Parking", "Dishwasher"],
            is_booked=False
        )
    ]
    
    try:
        db.session.add_all(sample_flats)
        db.session.commit()
        return jsonify({"message": "Database seeded successfully!", "count": len(sample_flats)}), 201
    except Exception as e:
        db.session.rollback()
        # This will return the specific database error to Postman
        return jsonify({"error": str(e)}), 500