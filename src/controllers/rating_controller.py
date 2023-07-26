from flask import Blueprint, request
from init import db 
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.rating import Rating, rating_schema, ratings_schema, rating_schema_exclude, ratings_schema_exclude
from controllers.track_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

ratings_bp = Blueprint('rating', __name__, url_prefix='/rating')

@ratings_bp.route('/')
@jwt_required()
def get_all_ratings():
    stmt = db.select(Rating)
    ratings = db.session.scalars(stmt)
    return ratings_schema_exclude.dump(ratings)

@ratings_bp.route('/<int:id>')
@jwt_required()
def get_track_via_rating(id):
    stmt = db.select(Rating).filter_by(id=id)
    rating = db.session.scalars(stmt)
    if rating:
        return ratings_schema.dump(rating)
    else:
        return {'error': f'Rating not found with id {id}'}, 404
    
@ratings_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_rating():
    try: 
        body_data = request.get_json()

        ratings = Rating(
            stars = body_data.get('stars')
        )
        
        db.session.add(ratings)
        db.session.commit()
        return rating_schema.dump(ratings), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': f"Rating '{ratings.stars}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409

@ratings_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_rating(id):
    body_data = request.get_json()
    stmt = db.select(Rating).filter_by(id=id)
    rating = db.session.scalar(stmt)
    if rating:
        rating.stars = body_data.get('stars') or rating.stars
        db.session.commit()
        return rating_schema_exclude.dump(rating)
    else: 
        return {'error': f'Difficulty with id {id} does not exist'}, 404