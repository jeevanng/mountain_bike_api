from flask import Blueprint, request
from init import db
from models.track import Track, track_schema, tracks_schema
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.comment_controller import comments_bp
import functools
from marshmallow import INCLUDE

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
    body_data = track_schema.load(request.get_json(), partial=True, unknown=INCLUDE)
    
    track = Track(
        name=body_data.get('name'),
        duration=body_data.get('duration'),
        description=body_data.get('description'),
        distance=body_data.get('distance'),
        climb=body_data.get('climb'),
        descent=body_data.get('descent'),
        difficulty_id=body_data.get('difficulty_id'),
        user_id=get_jwt_identity()
    )

    db.session.add(track)
    db.session.commit()

    return track_schema.dump(track), 201

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
        track.difficulty_id = body_data.get('difficulty_id') or track.difficulty_id
        db.session.commit()
        return track_schema.dump(track)
    else:
        return {'error': f'Track not found with id {id}'}, 404
    
# def authorise_as_admin():
#     user_id = get_jwt_identity()
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     return user.is_admin

