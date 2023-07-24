from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.difficulty import Difficulty, difficulty_schema, difficulties_schema, difficulties_schema_exclude
from controllers.track_controller import authorise_as_admin

difficulties_bp = Blueprint('difficulty', __name__, url_prefix='/difficulty')

@difficulties_bp.route('/')
@jwt_required()
def get_all_difficulties():
    stmt = db.select(Difficulty)
    difficulties = db.session.scalars(stmt)
    return difficulties_schema_exclude.dump(difficulties)

@difficulties_bp.route('/<int:id>')
@jwt_required()
def get_track_via_difficulty(id):
    stmt = db.select(Difficulty).filter_by(id=id)
    difficulty = db.session.scalar(stmt)
    if difficulty:
        return difficulty_schema.dump(difficulty)
    else:
        return {'error': f'Difficulty not found with id {id}'}, 404
    
@difficulties_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_difficulty():
    body_data = request.get_json()

    difficulty = Difficulty(
        difficulty = body_data.get('difficulty')
    )
    
    db.session.add(difficulty)
    db.session.commit()
    return difficulty_schema.dump(difficulty), 201
