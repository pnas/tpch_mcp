from flask import Blueprint, request, jsonify
from .. import db
from ..models import Customer

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.__dict__ for c in customers])

@bp.route('/<int:cust_key>', methods=['GET'])
def get_customer(cust_key):
    customer = Customer.query.get_or_404(cust_key)
    return jsonify(customer.__dict__)

@bp.route('/<int:cust_key>', methods=['PUT'])
def update_customer(cust_key):
    data = request.get_json()
    customer = Customer.query.get_or_404(cust_key)
    for key, value in data.items():
        setattr(customer, key, value)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@bp.route('/<int:cust_key>', methods=['DELETE'])
def delete_customer(cust_key):
    customer = Customer.query.get_or_404(cust_key)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})
