from flask import Blueprint, request, jsonify
from models import ParkingLocation, db

parking_routes = Blueprint('parking', __name__)

@parking_routes.route('/<int:location_id>', methods=['GET'])
def get_parking_locations(location_id):
    parkingLocation = ParkingLocation.query.get(location_id)
    if parkingLocation:
        return jsonify(parkingLocation.to_dict()), 200
    return jsonify({"error": "User not found"}), 404
    #return jsonify([location.to_dict() for location in locations]), 200

@parking_routes.route('/all', methods=['GET'])
def get_all_parking_locations():
    parkingLocations = ParkingLocation.query.all()
    return jsonify([parkingLocation.to_dict() for parkingLocation in parkingLocations]), 200


@parking_routes.route('/', methods=['POST'])
def add_parking_location():
    data = request.json
    new_location = ParkingLocation(**data)
    db.session.add(new_location)
    db.session.commit()
    return jsonify({"message": "Parking location added"}), 201
