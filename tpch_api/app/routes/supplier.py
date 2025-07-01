from flask import Blueprint, request, jsonify
from .. import db
from ..models import Supplier

bp = Blueprint('supplier', __name__, url_prefix='/supplier')

@bp.route('/', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = Supplier(**data)
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([s.__dict__ for s in suppliers])

@bp.route('/<int:supp_key>', methods=['GET'])
def get_supplier(supp_key):
    supplier = Supplier.query.get_or_404(supp_key)
    return jsonify(supplier.__dict__)

@bp.route('/<int:supp_key>', methods=['PUT'])
def update_supplier(supp_key):
    data = request.get_json()
    supplier = Supplier.query.get_or_404(supp_key)
    for key, value in data.items():
        setattr(supplier, key, value)
    db.session.commit()
    return jsonify({'message': 'Supplier updated successfully'})

@bp.route('/<int:supp_key>', methods=['DELETE'])
def delete_supplier(supp_key):
    supplier = Supplier.query.get_or_404(supp_key)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully'})
