from flask import Blueprint, request
from init import db
from models.track import Track, track_schema, tracks_schema
from models.user import User
from models.difficulty import Difficulty, difficulties_schema_exclude
from models.rating import Rating, ratings_schema_exclude
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.comment_controller import comments_bp
import functools
from marshmallow import INCLUDE, ValidationError
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

tracks_bp = Blueprint('tracks', __name__, url_prefix='/tracks')
tracks_bp.register_blueprint(comments_bp, url_prefix='/<int:track_id>/comments')

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

@tracks_bp.route('/')
def get_all_tracks():
    stmt = db.select(Track)
    tracks = db.session.scalars(stmt)
    return tracks_schema.dump(tracks)

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
        body_data = track_schema.load(request.get_json(), partial=True, unknown=INCLUDE)

        difficulty_str = body_data.get('difficulty_name')
        rating_str = body_data.get('stars')

        if difficulty_str:
            retrieved_difficulty_object = db.session.scalar(db.select(Difficulty).filter_by(difficulty_name=difficulty_str))
            if not retrieved_difficulty_object: 
                difficulty_list = db.session.scalars(db.select(Difficulty))
                difficulty_names = difficulties_schema_exclude.dump(difficulty_list)
                difficulty_array = []
                for difficulty in difficulty_names:
                    difficulty_array.append(difficulty['difficulty_name'])
                if difficulty_str not in difficulty_array:
                    return {'error': f'Not a valid difficulty. Must be one of the following; {difficulty_array}'}, 409
        else:
            return {'message': f'difficulty_name must be included.'}, 409
        
        if rating_str:
            retrieved_rating_object = db.session.scalar(db.select(Rating).filter_by(stars=rating_str))
            if not retrieved_rating_object:
                rating_list = db.session.scalars(db.select(Rating))
                rating_names = ratings_schema_exclude.dump(rating_list)
                rating_array = []
                for rating in rating_names:
                    rating_array.append(rating['stars'])
                if rating_str not in rating_array:
                    return {'error': f'Not a valid rating. Must be one of the following; {rating_array}'}, 409
        else:
            return {'message': f'stars column must be included.'}, 409
        
        track = Track(
            name=body_data.get('name'),
            duration=body_data.get('duration'),
            description=body_data.get('description'),
            distance=body_data.get('distance'),
            climb=body_data.get('climb'),
            descent=body_data.get('descent'),
            difficulty_id=retrieved_difficulty_object.id,
            rating_id=retrieved_rating_object.id,
            user_id=get_jwt_identity()
        )

        db.session.add(track)
        db.session.commit()

        return track_schema.dump(track), 201
    # except ValidationError as err:
    #     return {'error': err.messages}, 400
    except IntegrityError as err:
         if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} attribute is required' }, 409
    
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
        # CHECK TO SEE IF THIS WORKS, AS IN TWO ADMINS? WILL IT UPDATE WITH WHICH ADMIN PUT, PATCH
        track.user_id=get_jwt_identity()

        difficulty_str = body_data.get('difficulty_name')
        if difficulty_str: 
            retrieved_difficulty_object = db.session.scalar(db.select(Difficulty).filter_by(difficulty_name=difficulty_str))
            # If statement to handle when retrieved_difficulty_object is None 
            if retrieved_difficulty_object:
                track.difficulty_id = retrieved_difficulty_object.id 
            if not retrieved_difficulty_object: 
                difficulty_list = db.session.scalars(db.select(Difficulty))
                difficulty_names = difficulties_schema_exclude.dump(difficulty_list)
                difficulty_array = []
                for difficulty in difficulty_names:
                    difficulty_array.append(difficulty['difficulty_name'])
                if difficulty_str not in difficulty_array:
                    return {'error': f'Not a valid difficulty. Must be one of the following; {difficulty_array}'}, 409
        
        rating_str = body_data.get('stars')
        if rating_str:
            retrieved_rating_object = db.session.scalar(db.select(Rating).filter_by(stars=rating_str))
            if retrieved_rating_object:
                track.rating_id = retrieved_rating_object.id
            if not retrieved_rating_object:
                rating_list = db.session.scalars(db.select(Rating))
                rating_names = ratings_schema_exclude.dump(rating_list)
                rating_array = []
                for rating in rating_names:
                    rating_array.append(rating['stars'])
                if rating_str not in rating_array:
                    return {'error': f'Not a valid rating. Must be one of the following; {rating_array}'}, 409
        
        db.session.commit()
        return track_schema.dump(track)
    else:
        return {'error': f'Track not found with id {id}'}, 404
    
