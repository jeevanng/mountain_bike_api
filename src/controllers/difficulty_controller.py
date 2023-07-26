from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.difficulty import Difficulty, difficulty_schema, difficulties_schema, difficulties_schema_exclude
from controllers.track_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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
    try: 
        body_data = request.get_json()

        difficulty = Difficulty(
            difficulty_name = body_data.get('difficulty_name')
        )
        
        db.session.add(difficulty)
        db.session.commit()
        return difficulty_schema.dump(difficulty), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': f"Difficulty name '{difficulty.difficulty_name}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409
        
@difficulties_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_difficulty(id):
    stmt = db.select(Difficulty).filter_by(id=id)
    difficulty = db.session.scalar(stmt)
    if difficulty:
        db.session.delete(difficulty)
        db.session.commit()
        return {'message': f'Difficulty {difficulty.difficulty_name} was deleted successfully'}
    else: 
        return {'error': f'Track not found with id {id}'}, 404

@difficulties_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_difficulty(id):
    body_data = request.get_json()
    stmt = db.select(Difficulty).filter_by(id=id)
    difficulty = db.session.scalar(stmt)
    if difficulty:
        difficulty.difficulty_name = body_data.get('difficulty_name') or difficulty.difficulty_name
        db.session.commit()
        return difficulty_schema.dump(difficulty)
    else: 
        return {'error': f'Difficulty with id {id} does not exist'}, 404
