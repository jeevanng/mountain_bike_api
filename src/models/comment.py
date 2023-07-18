from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date = db.Column(db.Date)

    user_id = db.Column(db.Integer, ForeignKey=('users.id'), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey=('tracks.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    track = db.relationship('Track', back_populates='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    track = fields.Nested('TrackSchema', exclude=['comments'])

    class Meta:
        fields = ('id', 'content', 'date', 'track', 'user')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)