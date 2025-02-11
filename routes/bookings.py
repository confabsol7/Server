from flask import Blueprint, request, jsonify
from models import Booking, db
from datetime import datetime

booking_routes = Blueprint('bookings', __name__)

@booking_routes.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@booking_routes.route('/user/<string:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.start_time.desc()).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@booking_routes.route('/cancel/<int:booking_id>', methods=['PUT'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    booking.status = 'Cancelled'
    db.session.commit()
    return jsonify({"message": "Booking cancelled successfully"})


@booking_routes.route('/add', methods=['PUT'])
def create_booking():
    date_format = "%d-%m-%Y %H:%M"
    data = request.json
    pa_user_id = data.get("pa_user_id")
    parking_id = data.get("parking_id")
    start_time = datetime.strptime(data.get("start_time"), date_format)
    #start_time = data.get("start_time")
    duration = data.get("duration")
    total_price = data.get("total_price")

    new_booking = Booking(
        user_id=pa_user_id,
        location_id=parking_id,
        start_time=start_time,
        duration=duration,
        total_price=total_price,
        booking_type = 'hourly',
        payment_status = 'paid',
        payment_id = 'payemnt01'
    )
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Booking created successfully", "booking_id": new_booking.booking_id}), 201
