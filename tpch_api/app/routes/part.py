from flask import Blueprint, request, jsonify
from .. import db
from ..models import Part

bp = Blueprint('part', __name__, url_prefix='/part')

@bp.route('/', methods=['POST'])
def create_part():
    data = request.get_json()
    new_part = Part(**data)
    db.session.add(new_part)
    db.session.commit()
    return jsonify({'message': 'Part created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_parts():
    parts = Part.query.all()
    return jsonify([p.__dict__ for p in parts])

@bp.route('/<int:part_key>', methods=['GET'])
def get_part(part_key):
    part = Part.query.get_or_404(part_key)
    return jsonify(part.__dict__)

@bp.route('/<int:part_key>', methods=['PUT'])
def update_part(part_key):
    data = request.get_json()
    part = Part.query.get_or_404(part_key)
    for key, value in data.items():
        setattr(part, key, value)
    db.session.commit()
    return jsonify({'message': 'Part updated successfully'})

@bp.route('/<int:part_key>', methods=['DELETE'])
def delete_part(part_key):
    part = Part.query.get_or_404(part_key)
    db.session.delete(part)
    db.session.commit()
    return jsonify({'message': 'Part deleted successfully'})
