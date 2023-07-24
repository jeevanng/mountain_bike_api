from init import db, ma 
from marshmallow import fields

class Difficulty(db.Model):
    __tablename__= "difficulties"

    id = db.Column(db.Integer, primary_key=True)
    difficulty_name = db.Column(db.String, nullable=False, unique=True)

    tracks = db.relationship('Track', back_populates='difficulty')

class DifficultySchema(ma.Schema):
    tracks = fields.List(fields.Nested('TrackSchema', exclude=['difficulty']))

    class Meta:
        fields = ('id', 'difficulty_name', 'tracks')
        ordered = True

difficulty_schema = DifficultySchema()
difficulties_schema = DifficultySchema(many=True)
difficulties_schema_exclude = DifficultySchema(many=True, exclude=['tracks'])