from flask import Blueprint, request, jsonify
from models import Payment, db

payment_routes = Blueprint('payments', __name__)

@payment_routes.route('/', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments]), 200

@payment_routes.route('/', methods=['POST'])
def add_payment():
    data = request.json
    new_payment = Payment(**data)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Payment added"}), 201
