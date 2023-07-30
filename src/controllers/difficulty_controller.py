from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.difficulty import Difficulty, difficulty_schema, difficulties_schema, difficulty_schema_exclude, difficulties_schema_exclude
from controllers.track_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

difficulties_bp = Blueprint('difficulty', __name__, url_prefix='/difficulty')

# Get all difficulties that exist in the database
@difficulties_bp.route('/')
@jwt_required()
def get_all_difficulties():
    stmt = db.select(Difficulty)
    difficulties = db.session.scalars(stmt)
    return difficulties_schema_exclude.dump(difficulties)

# Get difficulty via id, and show the tracks that are associated with that difficulty. Get all the tracks with a certain difficulty
@difficulties_bp.route('/<int:id>')
@jwt_required()
def get_track_via_difficulty(id):
    # Query Difficulty model and entity and filter by id=id
    stmt = db.select(Difficulty).filter_by(id=id)
    difficulty = db.session.scalar(stmt)
    if difficulty:
        return difficulty_schema.dump(difficulty)
    else:
        return {'error': f'Difficulty not found with id {id}'}, 404

# Post new difficulty
@difficulties_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_difficulty():
    try: 
        body_data = difficulty_schema.load(request.get_json())

        difficulties = Difficulty(
            difficulty_name=body_data.get('difficulty_name')
        )
        
        db.session.add(difficulties)
        db.session.commit()
        return difficulty_schema_exclude.dump(difficulties), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': f"Difficulty name '{difficulties.difficulty_name}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409
    
# Delete difficulty
@difficulties_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_difficulty(id):
    try:
        # Query Difficulty model and entity and filter by id=id
        stmt = db.select(Difficulty).filter_by(id=id)
        difficulty = db.session.scalar(stmt)
        if difficulty:
            db.session.delete(difficulty)
            db.session.commit()
            return {'message': f'Difficulty {difficulty.difficulty_name} was deleted successfully'}
        else: 
            return {'error': f'Difficulty not found with id {id}'}, 404
    except IntegrityError as err:
        # If the difficulty being deleted is linked to a track, the value will become null, which will violate NOT NULL constraint. 
        # Show error message below. 
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            db.session.rollback()
            return {'error': 'Unable to delete',
                    'message': f'Track/s have the difficulty name {difficulty.difficulty_name} (id of {id}) that you are trying to delete. Please edit the track/s with those difficulties before deleting'}, 409

@difficulties_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_difficulty(id):
    body_data = difficulty_schema.load(request.get_json())
    # Query Difficulty model and entity and filter by id=id
    stmt = db.select(Difficulty).filter_by(id=id)
    difficulty = db.session.scalar(stmt)
    if difficulty:
        difficulty.difficulty_name = body_data.get('difficulty_name') or difficulty.difficulty_name
        db.session.commit()
        return difficulty_schema_exclude.dump(difficulty)
    else: 
        return {'error': f'Difficulty with id {id} does not exist'}, 404

