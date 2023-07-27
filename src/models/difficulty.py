from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Difficulty(db.Model):
    __tablename__= "difficulties"

    id = db.Column(db.Integer, primary_key=True)
    difficulty_name = db.Column(db.String, nullable=False, unique=True)

    tracks = db.relationship('Track', back_populates='difficulty')

class DifficultySchema(ma.Schema):
    tracks = fields.List(fields.Nested('TrackSchema', exclude=['difficulty']))
    difficulty_name = fields.String(required=True, validate=And(
        Length(min=2, error='Difficulty name must be at least 2 characters long'),
        Regexp("^[a-zA-Z0-9'. ]+$", error="Only letters, fullstops, apostrophe's, spaces and numbers are allowed")))
    
    class Meta:
        fields = ('id', 'difficulty_name', 'tracks')
        ordered = True

difficulty_schema = DifficultySchema()
difficulty_schema_exclude = DifficultySchema(exclude=['tracks'])
difficulties_schema = DifficultySchema(many=True)
difficulties_schema_exclude = DifficultySchema(many=True, exclude=['tracks'])