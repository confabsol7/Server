from flask import Blueprint, request, jsonify
from models import User, db
import logging
from sqlalchemy import text


logging.basicConfig(level=logging.DEBUG)

profile_routes = Blueprint('profile', __name__)

@profile_routes.route('/<string:pa_user_id>', methods=['GET'])
def get_profile(pa_user_id):
    #user = User.query.filter_by(pa_user_id = pa_user_id).get_children()
    user = db.one_or_404(db.select(User).filter_by(pa_user_id=pa_user_id))
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@profile_routes.route('/<string:pa_user_id>', methods=['PUT'])
def update_profile(pa_user_id):
    #user = User.query.get(user_id)
    user = db.one_or_404(db.select(User).filter_by(pa_user_id=pa_user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.name = data.get('name', user.name)
    user.phone = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.to_dict()}), 200


@profile_routes.route('/register', methods=['PUT'])
def add_user():
    try:
        data = request.get_json()

        # ✅ Log the incoming data
        logging.info(f"Received parking data: {data}")

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # ✅ Validate required fields
        required_fields = ["pa_user_id", "name", "phone", "email"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            logging.info(f"Missing fields", missing_fields)
            #return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # ✅ Convert numeric & enum values properly
        try:
            pa_user_id = data["pa_user_id"]
            name = data["name"]
            phone = data.get("phone", 0)
            email = data["email"]
        except ValueError as e:
            logging.info(f"Invalid data fields")
            #return jsonify({"error": f"Invalid data type: {str(e)}"}), 400

        # ✅ Create a new ParkingLocation object
        new_user = User(
            pa_user_id=pa_user_id,
            name=name,
            password_hash = '',
            phone=phone,
            email=email,
            role='car_owner'
        )

        # ✅ Add and commit to the database
        db.session.add(new_user)
        db.session.commit()

        logging.info(f"New parking added with ID: {new_user.pa_user_id}")

        return jsonify({"message": "Parking added successfully", "location_id": new_user.pa_user_id}), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding parking: {str(e)}")
        return jsonify({"error": str(e)}), 400