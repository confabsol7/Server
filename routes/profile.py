from flask import Blueprint, request, jsonify
from models import User, db

profile_routes = Blueprint('profile', __name__)

@profile_routes.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@profile_routes.route('/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.name = data.get('name', user.name)
    user.phone = data.get('phone', user.phone)
    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.to_dict()}), 200
