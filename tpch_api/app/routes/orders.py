from flask import Blueprint, request, jsonify
from .. import db
from ..models import Orders

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Orders(**data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_orders():
    orders = Orders.query.all()
    return jsonify([o.__dict__ for o in orders])

@bp.route('/<int:order_key>', methods=['GET'])
def get_order(order_key):
    order = Orders.query.get_or_404(order_key)
    return jsonify(order.__dict__)

@bp.route('/<int:order_key>', methods=['PUT'])
def update_order(order_key):
    data = request.get_json()
    order = Orders.query.get_or_404(order_key)
    for key, value in data.items():
        setattr(order, key, value)
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@bp.route('/<int:order_key>', methods=['DELETE'])
def delete_order(order_key):
    order = Orders.query.get_or_404(order_key)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})
