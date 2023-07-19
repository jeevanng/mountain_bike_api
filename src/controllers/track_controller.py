from flask import Blueprint, request
from init import db
from models.track import Track, track_schema, tracks_schema
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.comment import Comment, comment_schema, comments_schema
from datetime import date

tracks_bp = Blueprint('tracks', __name__, url_prefix='/tracks')


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
def create_track():
    body_data = request.get_json()
    track = Track(
        name=body_data.get('name'),
        duration=body_data.get('duration'),
        description=body_data.get('description'),
        distance=body_data.get('distance'),
        climb=body_data.get('climb'),
        descent=body_data.get('descent'),
        user_id=get_jwt_identity()
    )

    db.session.add(track)
    db.session.commit()

    return track_schema.dump(track), 201

@tracks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
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
def update_one_track(id):
    body_data = request.get_json()
    stmt = db.select(Track).filter_by(id=id)
    track = db.session.scalar(stmt)
    if track: 
        track.name = body_data.get('name') or track.name
        track.duration = body_data.get('duration') or track.duration
        track.description = body_data.get('description') or track.description
        track.distance = body_data.get('distance') or track.distance
        track.climb = body_data.get('climb') or track.climb
        track.descent = body_data.get('descent') or track.descent
        db.session.commit()
        return track_schema.dump(track)
    else:
        return {'error': f'Track not found with id {id}'}, 404

@tracks_bp.route('/<int:track_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(track_id):
    body_data = request.get_json()
    stmt = db.select(Track).filter_by(id=track_id)
    track = db.session.scalar(stmt)
    if track:
        comment = Comment(
            message=body_data.get('message'),
            date=date.today(),
            user_id=get_jwt_identity(),
            track_id=track.id
        )

        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {'error': f'Track with {track_id} does not exist'}, 404
    
@tracks_bp.route('/<int:track_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(track_id, comment_id):
    current_user_id = get_jwt_identity()
    
    stmt = db.select(Comment).filter_by(id=comment_id, user_id=current_user_id)
    comment = db.session.scalar(stmt)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'{comment.message} deleted successfully.'}
    else:
        return {'error': f'Comment with id {comment_id} not found or you are not authorised to delete the comment.'}, 404

@tracks_bp.route('/<int:track_id>/comments/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_comment(track_id, comment_id):
    current_user_id = get_jwt_identity()

    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id, user_id=current_user_id)
    comment = db.session.scalar(stmt)

    if comment:
        comment.message = body_data.get('message') or comment.message
        db.session.commit()
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment with comment id {comment_id} does not exist.'}, 404
    