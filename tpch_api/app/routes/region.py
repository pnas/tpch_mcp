from flask import Blueprint, request, jsonify
from .. import db
from ..models import Region

bp = Blueprint('region', __name__, url_prefix='/region')

@bp.route('/', methods=['POST'])
def create_region():
    data = request.get_json()
    new_region = Region(
        r_regionkey=data['r_regionkey'],
        r_name=data['r_name'],
        r_comment=data.get('r_comment')
    )
    db.session.add(new_region)
    db.session.commit()
    return jsonify({'message': 'Region created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_regions():
    regions = Region.query.all()
    return jsonify([{'r_regionkey': r.r_regionkey, 'r_name': r.r_name, 'r_comment': r.r_comment} for r in regions])

@bp.route('/<int:region_key>', methods=['GET'])
def get_region(region_key):
    region = Region.query.get_or_404(region_key)
    return jsonify({'r_regionkey': region.r_regionkey, 'r_name': region.r_name, 'r_comment': region.r_comment})

@bp.route('/<int:region_key>', methods=['PUT'])
def update_region(region_key):
    data = request.get_json()
    region = Region.query.get_or_404(region_key)
    region.r_name = data['r_name']
    region.r_comment = data.get('r_comment')
    db.session.commit()
    return jsonify({'message': 'Region updated successfully'})

@bp.route('/<int:region_key>', methods=['DELETE'])
def delete_region(region_key):
    region = Region.query.get_or_404(region_key)
    db.session.delete(region)
    db.session.commit()
    return jsonify({'message': 'Region deleted successfully'})
