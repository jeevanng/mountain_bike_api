from init import db, ma 
from marshmallow import fields, Schema, post_dump, validates
from marshmallow.validate import Length, And, Regexp
from sqlalchemy import Time
import re
from marshmallow.exceptions import ValidationError

class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(Time)
    description = db.Column(db.Text)
    distance = db.Column(db.Integer, nullable=False)
    climb = db.Column(db.Integer, nullable=False)
    descent = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='tracks')
    comments = db.relationship('Comment', back_populates='track', cascade='all, delete')

class TrackSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['track']))

    name = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp("^[a-zA-Z0-9'. ]+$", error="Only letters, fullstops, apostrophe's, spaces and numbers are allowed")
    ))
    description = fields.String(validate=Regexp("^[a-zA-Z0-9'. ]+$", error="Only letters, fullstops, apostrophe's, spaces and numbers are allowed"))
    duration = fields.Time(format='%H:%M:%S')
    distance = fields.Integer(required=True)
    climb = fields.Integer(required=True)
    descent = fields.Integer(required=True)
    
    @post_dump
    def format_distance_metres(self, data, **kwargs):
        data['distance'] = f"{data['distance']}m"
        return data
    
    @post_dump
    def format_climb_metres(self, data, **kwargs):
        data['climb'] = f"{data['climb']}m"
        return data
    
    @post_dump
    def format_descent_metres(self, data, **kwargs):
        data['descent'] = f"{data['descent']}m"
        return data

    class Meta:
        fields = ('id', 'name', 'duration', 'description', 'distance', 'climb', 'descent', 'user', 'comments')
        ordered = True

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)