from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        role=data['role'],
        password_hash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    return jsonify({"error": "Invalid credentials"}), 401
