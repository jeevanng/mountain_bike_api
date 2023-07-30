from init import db, ma 
from marshmallow import fields, Schema, post_dump, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from sqlalchemy import Time

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
    difficulty_id = db.Column(db.Integer, db.ForeignKey('difficulties.id'), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    
    user = db.relationship('User', back_populates='tracks')
    # When a track is deleted, delete all the comments linked to that track
    comments = db.relationship('Comment', back_populates='track', cascade='all, delete')
    difficulty = db.relationship('Difficulty', back_populates='tracks')
    rating = db.relationship('Rating', back_populates='tracks')
    location = db.relationship('Location', back_populates='tracks')
    # When a track is deleted, delete all recommendations linked to tha track 
    recommendations = db.relationship('Recommendation', back_populates='track', cascade='all, delete')

class TrackSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['track']))
    difficulty = fields.Nested('DifficultySchema', exclude=['tracks'])
    rating = fields.Nested('RatingSchema', exclude=['tracks'])
    location = fields.Nested('LocationSchema', exclude=['tracks'])
    recommendations = fields.List(fields.Nested('RecommendationSchema', exclude=['track']))

    name = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp("^[a-zA-Z0-9'. ]+$", error="Only letters, fullstops, apostrophe's, spaces and numbers are allowed")
    ))
    description = fields.String(validate=Regexp("^[a-zA-Z0-9'. ]+$", error="Only letters, fullstops, apostrophe's, spaces and numbers are allowed"))
    duration = fields.Time(format='%H:%M:%S')
    distance = fields.Integer(required=True)
    climb = fields.Integer(required=True)
    descent = fields.Integer(required=True)
    
    # This will return the "m" for distance, climb and descent. Indicating it is metres
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
        fields = ('id', 'name', 'duration', 'description', 'distance', 'climb', 'descent', 'difficulty', 'rating', 'location', 'recommendations', 'user', 'comments')
        ordered = True

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)