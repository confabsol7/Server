from flask import Blueprint, request, jsonify
from models import Advertisement, db

ad_routes = Blueprint('ads', __name__)

@ad_routes.route('/', methods=['GET'])
def get_ads():
    ads = Advertisement.query.all()
    return jsonify([ad.to_dict() for ad in ads]), 200

@ad_routes.route('/', methods=['POST'])
def add_ad():
    data = request.json
    new_ad = Advertisement(**data)
    db.session.add(new_ad)
    db.session.commit()
    return jsonify({"message": "Ad added"}), 201
