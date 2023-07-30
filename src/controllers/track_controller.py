from flask import Blueprint, request
from init import db
from models.track import Track, track_schema, tracks_schema
from models.user import User
from models.difficulty import Difficulty, difficulties_schema_exclude
from models.rating import Rating, ratings_schema_exclude
from models.location  import Location, locations_schema_exclude
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.comment_controller import comments_bp
import functools
from marshmallow import INCLUDE, ValidationError
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

# Blueprints for routes
tracks_bp = Blueprint('tracks', __name__, url_prefix='/tracks')
tracks_bp.register_blueprint(comments_bp, url_prefix='/<int:track_id>/comments')

# Function to check whether user is admin
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform that function. Only an admin has permission.'}, 403
    return wrapper

# Takes difficulty_str as argument, representing the difficulty name that needs to be validated
def validate_difficulty(difficulty_str):
    # If difficulty_str is empty, return the error message below
    if not difficulty_str:
        return {'message': 'difficulty_name must be included.'}, 409

    # Query database that matches the filters below (difficulty_name = difficulty_str)
    retrieved_difficulty_object = db.session.scalar(db.select(Difficulty).filter_by(difficulty_name=difficulty_str))
    # If retrieved_difficulty_object does not exist, execute code below
    if not retrieved_difficulty_object:
        # Obtain all difficulties in the entity
        difficulty_list = db.session.scalars(db.select(Difficulty))
        difficulty_names = difficulties_schema_exclude.dump(difficulty_list)
        # Create an array containing all the difficulties possible
        difficulty_array = [difficulty['difficulty_name'] for difficulty in difficulty_names]
        # Check to see whether difficulty_str exists in the array. If not return error message and showing list of acceptable difficulties
        if difficulty_str not in difficulty_array:
            return {'error': f'Not a valid difficulty. Must be one of the following: {difficulty_array}'}, 409
    # If the difficulty_str is found in the queried database, it means the difficulty name is valid and the function returns none, indicating validation was successful.
    return None

# This function will do the same as above, except for ratings/stars
def validate_rating(rating_str):
    if not rating_str:
        return {'message': 'stars column must be included.'}, 409

    retrieved_rating_object = db.session.scalar(db.select(Rating).filter_by(stars=rating_str))
    if not retrieved_rating_object:
        rating_list = db.session.scalars(db.select(Rating))
        rating_names = ratings_schema_exclude.dump(rating_list)
        rating_array = [rating['stars'] for rating in rating_names]
        if rating_str not in rating_array:
            return {'error': f'Not a valid rating. Must be one of the following: {rating_array}'}, 409
    return None

# This function will do the same as above except for locations
def validate_location(location_str):
    if not location_str:
        return {'message': 'location_name must be included.'}, 409

    retrieved_location_object = db.session.scalar(db.select(Location).filter_by(location_name=location_str))
    if not retrieved_location_object:
        location_list = db.session.scalars(db.select(Location))
        location_names = locations_schema_exclude.dump(location_list)
        location_array = [location['location_name'] for location in location_names]
        if location_str not in location_array:
            return {'error': f'Not a valid location. Must be one of the following: {location_array}'}, 409
    return None

# Get all tracks that exist in the database
@tracks_bp.route('/')
def get_all_tracks():
    stmt = db.select(Track)
    tracks = db.session.scalars(stmt)
    return tracks_schema.dump(tracks)

# Get track by ID 
@tracks_bp.route('/<int:id>')
def get_one_track(id):
    stmt = db.select(Track).filter_by(id=id)
    track = db.session.scalar(stmt)
    if track: 
        return track_schema.dump(track)
    else:
        return {'error': f'Track not found with id {id}'}, 404
    

@tracks_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_track():
    try:
        # partial and unknown parameters included 
        body_data = track_schema.load(request.get_json(), partial=True, unknown=INCLUDE)

        difficulty_str = body_data.get('difficulty_name')
        rating_str = body_data.get('stars')
        location_str = body_data.get('location_name')
        
        # Calls validate_difficulty function and passes difficulty_str as an argument
        difficulty_error = validate_difficulty(difficulty_str)
        # Checks to see whether difficulty_error has a value. If it does, it means the difficulty_name is not valid and has an error.
        if difficulty_error:
            # Return the error generated by the function
            return difficulty_error

        # As above but for rating_str
        rating_error = validate_rating(rating_str)
        if rating_error:
            return rating_error

        # As above but for location_str
        location_error = validate_location(location_str)
        if location_error:
            return location_error
        
        # If no errors are returned, difficulty_str, rating_str and location_str exist in the database and can be queried and returned as objects
        retrieved_difficulty_object = db.session.scalar(db.select(Difficulty).filter_by(difficulty_name=difficulty_str))
        retrieved_rating_object = db.session.scalar(db.select(Rating).filter_by(stars=rating_str))
        retrieved_location_object = db.session.scalar(db.select(Location).filter_by(location_name=location_str))


        track = Track(
            name=body_data.get('name'),
            duration=body_data.get('duration'),
            description=body_data.get('description'),
            distance=body_data.get('distance'),
            climb=body_data.get('climb'),
            descent=body_data.get('descent'),
            difficulty_id=retrieved_difficulty_object.id,
            rating_id=retrieved_rating_object.id,
            location_id=retrieved_location_object.id,
            user_id=get_jwt_identity()
        )

        db.session.add(track)
        db.session.commit()

        return track_schema.dump(track), 201
    except IntegrityError as err:
         if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} attribute is required' }, 409

# Delete a track
@tracks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_one_track(id):
    stmt = db.select(Track).filter_by(id=id)
    track = db.session.scalar(stmt)
    if track:
        db.session.delete(track)
        db.session.commit()
        return {'message': f'Track {track.name} was deleted successfully'}
    else: 
        return {'error': f'Track not found with id {id}'}, 404

# Edit/update track 
@tracks_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_one_track(id):
    body_data = track_schema.load(request.get_json(), partial=True, unknown=INCLUDE)
    stmt = db.select(Track).filter_by(id=id)
    track = db.session.scalar(stmt)

    if track: 
        track.name = body_data.get('name') or track.name
        track.duration = body_data.get('duration') or track.duration
        track.description = body_data.get('description') or track.description
        track.distance = body_data.get('distance') or track.distance
        track.climb = body_data.get('climb') or track.climb
        track.descent = body_data.get('descent') or track.descent
        # This will update the user details to equal the admin user who is updating the track
        track.user_id=get_jwt_identity()

        # Retrieve the value of difficulty_name from body_data (What is entered into front end)
        difficulty_str = body_data.get('difficulty_name')
        # If it exists, check whether it is a non-empty value
        if difficulty_str:
            # Check whether the difficulty_name in the body_data is a valid difficulty in the database
            difficulty_error = validate_difficulty(difficulty_str)
            if difficulty_error:
                return difficulty_error

            # After difficulty_name has passed validation, query database according to the filter parameters and retrieve object
            retrieved_difficulty_object = db.session.scalar(db.select(Difficulty).filter_by(difficulty_name=difficulty_str))
            if retrieved_difficulty_object:
                # Update difficulty_id to equal the retrieved object id (which will be filtered by the difficulty_str)
                track.difficulty_id = retrieved_difficulty_object.id

        # Same as above but for stars/ratings
        rating_str = body_data.get('stars')
        if rating_str:
            rating_error = validate_rating(rating_str)
            if rating_error:
                return rating_error

            retrieved_rating_object = db.session.scalar(db.select(Rating).filter_by(stars=rating_str))
            if retrieved_rating_object:
                track.rating_id = retrieved_rating_object.id

        # Same as above but for location
        location_str = body_data.get('location_name')
        if location_str:
            location_error = validate_location(location_str)
            if location_error:
                return location_error

            retrieved_location_object = db.session.scalar(db.select(Location).filter_by(location_name=location_str))
            if retrieved_location_object:
                track.location_id = retrieved_location_object.id
        
        db.session.commit()
        return track_schema.dump(track)
    else:
        return {'error': f'Track not found with id {id}'}, 404
    
