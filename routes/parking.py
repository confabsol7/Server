from flask import Blueprint, request, jsonify
from models import ParkingLocation, db
import logging

logging.basicConfig(level=logging.DEBUG)

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


@parking_routes.route('/add/<int:manager_id>', methods=['PUT'])
def add_parking(manager_id):
    try:
        data = request.get_json()

        # ✅ Log the incoming data
        logging.info(f"Received parking data: {data}")

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # ✅ Validate required fields
        required_fields = ["manager_id", "address", "latitude", "longitude", "total_spots", "available_spots", "zipcode", "category"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            logging.info(f"Missing fields")
            #return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # ✅ Convert numeric & enum values properly
        try:
            latitude = float(data["lattitude"])
            longitude = float(data["longitudede"])
            hourly_price = float(data.get("hourly_price", 0))
            daily_price = float(data.get("daily_price", 0))
            weekly_price = float(data.get("weekly_price", 0))
            monthly_price = float(data.get("monthly_price", 0))
            rating = float(data.get("rating", 0))
            category = data["category"] if data["category"] in ["Free", "Paid"] else "Paid"  # Default to Paid
        except ValueError as e:
            logging.info(f"Invalid data fields")
            #return jsonify({"error": f"Invalid data type: {str(e)}"}), 400

        # ✅ Create a new ParkingLocation object
        new_parking = ParkingLocation(
            manager_id=data["managerid"],
            address=data["address"],
            latitude=latitude,
            longitude=longitude,
            total_spots=data["total_spots"],
            available_spots=data["availableSpots"],
            hourly_price=hourly_price,
            daily_price=daily_price,
            weekly_price=weekly_price,
            monthly_price=monthly_price,
            zipcode=data["zipcode"],
            category=category,
            rating=rating
        )

        # ✅ Add and commit to the database
        db.session.add(new_parking)
        db.session.commit()

        logging.info(f"New parking added with ID: {new_parking.location_id}")

        return jsonify({"message": "Parking added successfully", "location_id": new_parking.location_id}), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding parking: {str(e)}")
        return jsonify({"error": str(e)}), 400
