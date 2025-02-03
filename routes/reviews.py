from flask import Blueprint, request, jsonify
from models import Review, db

review_routes = Blueprint('reviews', __name__)

@review_routes.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200

@review_routes.route('/', methods=['POST'])
def add_review():
    data = request.json
    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review added"}), 201
