from flask import Blueprint, request, jsonify
from models import mycars, db

mycars_routes = Blueprint('mycars', __name__)

@mycars_routes.route('/all', methods=['GET'])
def get_mycars():
    Mycars = mycars.query.all()
    return jsonify([Mycars.to_dict() for mycar in Mycars]), 200

@mycars_routes.route('/<int:user_id>', methods=['GET'])
def get_mycars_userid(user_id):
    Mycars = mycars.query.filter_by(user_id=user_id).all()
    if mycars:
        return jsonify([Mycar.to_dict() for Mycar in Mycars]), 200
    return jsonify({"error": "cars not found"}), 404

    
#@mycars_routes.route('/', methods=['POST'])
@mycars_routes.route('/<int:user_id>', methods=['POST'])
def add_mycar():
    data = request.get_json()  # ✅ Ensure JSON request is properly extracted
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # ✅ Extract fields safely
    model = data.get("model")
    carnumber = data.get("carnumber")
    user_id = data.get("user_id")  # Ensure user_id is provided

    if not model or not carnumber or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_car = mycars(model=model, carnumber=carnumber, user_id=user_id)
        db.session.add(new_car)
        db.session.commit()
        return jsonify({"message": "Car added successfully", "car_id": new_car.carid}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
