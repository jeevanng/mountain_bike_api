from init import db, ma 
from marshmallow import fields 

class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)
    description = db.Column(db.Text)
    distance = db.Column(db.Integer)
    climb = db.Column(db.Integer)
    descent = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='tracks')

class TrackSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])

    class Meta:
        fields = ('id', 'name', 'duration', 'description', 'distance', 'climb', 'descent', 'user')
        ordered = True

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)