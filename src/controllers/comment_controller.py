from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment, comment_schema, comments_schema
from models.track import Track
from models.user import User
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
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        current_user_id = get_jwt_identity()
        current_user = db.session.scalar(db.select(User).filter_by(id=current_user_id))

        if current_user.id != comment.user_id and not current_user.is_admin:
            return {'error': 'Only the owner of a card, or an admin can delete the comment.'}
        else:
            db.session.delete(comment)
            db.session.commit()
        return {'message': f'{comment.message} deleted successfully.'}
    else:
        return {'error': f'Comment with id {comment_id} not found.'}, 404

@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_comment(track_id, comment_id):

    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        if str(comment.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of a card can update/edit the comment.'}
        else:
            comment.message = body_data.get('message') or comment.message
            db.session.commit()
            return comment_schema.dump(comment)
    else:
        return {'error': f'Comment with comment id {comment_id} does not exist.'}, 404
    