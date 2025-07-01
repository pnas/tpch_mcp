from flask import Blueprint, request, jsonify
from .. import db
from ..models import Partsupp

bp = Blueprint('partsupp', __name__, url_prefix='/partsupp')

@bp.route('/', methods=['POST'])
def create_partsupp():
    data = request.get_json()
    new_partsupp = Partsupp(**data)
    db.session.add(new_partsupp)
    db.session.commit()
    return jsonify({'message': 'Partsupp created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_partsupps():
    partsupps = Partsupp.query.all()
    return jsonify([ps.__dict__ for ps in partsupps])

@bp.route('/<int:part_key>/<int:supp_key>', methods=['GET'])
def get_partsupp(part_key, supp_key):
    partsupp = Partsupp.query.get_or_404((part_key, supp_key))
    return jsonify(partsupp.__dict__)

@bp.route('/<int:part_key>/<int:supp_key>', methods=['PUT'])
def update_partsupp(part_key, supp_key):
    data = request.get_json()
    partsupp = Partsupp.query.get_or_404((part_key, supp_key))
    for key, value in data.items():
        setattr(partsupp, key, value)
    db.session.commit()
    return jsonify({'message': 'Partsupp updated successfully'})

@bp.route('/<int:part_key>/<int:supp_key>', methods=['DELETE'])
def delete_partsupp(part_key, supp_key):
    partsupp = Partsupp.query.get_or_404((part_key, supp_key))
    db.session.delete(partsupp)
    db.session.commit()
    return jsonify({'message': 'Partsupp deleted successfully'})
