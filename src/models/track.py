from init import db, ma 
from marshmallow import fields, Schema
from sqlalchemy import Time

class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(Time)
    description = db.Column(db.Text)
    distance = db.Column(db.Integer)
    climb = db.Column(db.Integer)
    descent = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='tracks')

class TrackSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])

    def format_distance_metres(self, obj):
        return f"{obj.distance}m"
    
    def format_climb_metres(self, obj):
        return f"{obj.climb}m"
    
    def format_descent_metres(self, obj):
        return f"{obj.descent}m"

    distance = fields.Method('format_distance_metres')
    climb = fields.Method('format_climb_metres')
    descent = fields.Method('format_descent_metres')

    class Meta:
        fields = ('id', 'name', 'duration', 'description', 'distance', 'climb', 'descent', 'user')
        ordered = True

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)