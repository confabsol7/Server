from flask import Blueprint, request, jsonify
from models import Booking, db

booking_routes = Blueprint('bookings', __name__)

@booking_routes.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

@booking_routes.route('/', methods=['POST'])
def add_booking():
    data = request.json
    new_booking = Booking(**data)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Booking created"}), 201
