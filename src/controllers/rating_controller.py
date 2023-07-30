from flask import Blueprint, request
from init import db 
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.rating import Rating, rating_schema, ratings_schema, rating_schema_exclude, ratings_schema_exclude
from controllers.track_controller import authorise_as_admin
from models.track import Track 
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

ratings_bp = Blueprint('rating', __name__, url_prefix='/rating')

# Get all ratings 
@ratings_bp.route('/')
@jwt_required()
def get_all_ratings():
    stmt = db.select(Rating)
    ratings = db.session.scalars(stmt)
    return ratings_schema_exclude.dump(ratings)

# Get rating and all the tracks associated to that rating
@ratings_bp.route('/<int:id>')
@jwt_required()
def get_track_via_rating(id):
    stmt = db.select(Rating).filter_by(id=id)
    rating = db.session.scalars(stmt)
    if rating:
        return ratings_schema.dump(rating)
    else:
        return {'error': f'Rating not found with id {id}'}, 404
    
# Post new rating
@ratings_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_rating():
    try: 
        body_data = request.get_json()

        ratings = Rating(
            stars=body_data.get('stars')
        )
        
        db.session.add(ratings)
        db.session.commit()
        return rating_schema_exclude.dump(ratings), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': f"Rating '{ratings.stars}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required' }, 409
    except DataError as err:
        return {'error': 'Not a valid integer. Please enter a valid number'}

# Edit/update rating
@ratings_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_rating(id):
    try:
        body_data = request.get_json()
        stmt = db.select(Rating).filter_by(id=id)
        rating = db.session.scalar(stmt)
        if rating:
            rating.stars = body_data.get('stars') or rating.stars
            db.session.commit()
            return rating_schema_exclude.dump(rating)
        else: 
            return {'error': f'Rating with id {id} does not exist'}, 404
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': f'Stars with value of {body_data.get("stars")} already exists. Enter a non-existing value'}
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required' }, 409
    except DataError as err:
        return {'error': 'Not a valid integer. Please enter a valid number'}
        
@ratings_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_rating(id):
    try:
        stmt = db.select(Rating).filter_by(id=id)
        rating = db.session.scalar(stmt)
        if rating:
            db.session.delete(rating)
            db.session.commit()
            return {'message': f'Rating {rating.stars} was deleted successfully'}
        else:
            return {'message': f'Rating not found with id {id}'}, 404
    except IntegrityError as err:
        # If a user tries to delete a rating, where that rating is the foreign key of a track. It will become null, and violate the 
        # not null violation. Thus provide the code error below.
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            db.session.rollback()
            return {'error': 'Unable to delete',
                    'message': f'Track/s have the stars value {rating.stars} (id of {id}) that you are trying to delete. Please edit the track/s with those ratings before deleting'}, 409
