from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment, comment_schema, comments_schema
from models.track import Track
from datetime import date

comments_bp = Blueprint('comments', __name__,)

@comments_bp.route('/', methods=['POST'])
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
    
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
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

@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
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
    