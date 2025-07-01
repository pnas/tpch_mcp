from flask import Blueprint, request, jsonify
from .. import db
from ..models import Nation

bp = Blueprint('nation', __name__, url_prefix='/nation')

@bp.route('/', methods=['POST'])
def create_nation():
    data = request.get_json()
    new_nation = Nation(
        n_nationkey=data['n_nationkey'],
        n_name=data['n_name'],
        n_regionkey=data['n_regionkey'],
        n_comment=data.get('n_comment')
    )
    db.session.add(new_nation)
    db.session.commit()
    return jsonify({'message': 'Nation created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_nations():
    nations = Nation.query.all()
    return jsonify([{'n_nationkey': n.n_nationkey, 'n_name': n.n_name, 'n_regionkey': n.n_regionkey, 'n_comment': n.n_comment} for n in nations])

@bp.route('/<int:nation_key>', methods=['GET'])
def get_nation(nation_key):
    nation = Nation.query.get_or_404(nation_key)
    return jsonify({'n_nationkey': nation.n_nationkey, 'n_name': nation.n_name, 'n_regionkey': nation.n_regionkey, 'n_comment': nation.n_comment})

@bp.route('/<int:nation_key>', methods=['PUT'])
def update_nation(nation_key):
    data = request.get_json()
    nation = Nation.query.get_or_404(nation_key)
    nation.n_name = data['n_name']
    nation.n_regionkey = data['n_regionkey']
    nation.n_comment = data.get('n_comment')
    db.session.commit()
    return jsonify({'message': 'Nation updated successfully'})

@bp.route('/<int:nation_key>', methods=['DELETE'])
def delete_nation(nation_key):
    nation = Nation.query.get_or_404(nation_key)
    db.session.delete(nation)
    db.session.commit()
    return jsonify({'message': 'Nation deleted successfully'})
