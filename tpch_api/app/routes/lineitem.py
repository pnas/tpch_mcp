from flask import Blueprint, request, jsonify
from .. import db
from ..models import Lineitem

bp = Blueprint('lineitem', __name__, url_prefix='/lineitem')

@bp.route('/', methods=['POST'])
def create_lineitem():
    data = request.get_json()
    new_lineitem = Lineitem(**data)
    db.session.add(new_lineitem)
    db.session.commit()
    return jsonify({'message': 'Lineitem created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_lineitems():
    lineitems = Lineitem.query.all()
    return jsonify([li.__dict__ for li in lineitems])

@bp.route('/<int:order_key>/<int:line_number>', methods=['GET'])
def get_lineitem(order_key, line_number):
    lineitem = Lineitem.query.get_or_404((order_key, line_number))
    return jsonify(lineitem.__dict__)

@bp.route('/<int:order_key>/<int:line_number>', methods=['PUT'])
def update_lineitem(order_key, line_number):
    data = request.get_json()
    lineitem = Lineitem.query.get_or_404((order_key, line_number))
    for key, value in data.items():
        setattr(lineitem, key, value)
    db.session.commit()
    return jsonify({'message': 'Lineitem updated successfully'})

@bp.route('/<int:order_key>/<int:line_number>', methods=['DELETE'])
def delete_lineitem(order_key, line_number):
    lineitem = Lineitem.query.get_or_404((order_key, line_number))
    db.session.delete(lineitem)
    db.session.commit()
    return jsonify({'message': 'Lineitem deleted successfully'})
