from init import db, ma 
from marshmallow import fields

class Difficulty(db.Model):
    __tablename__= "difficulties"

    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String, nullable=False)

    tracks = db.relationship('Track', back_populates='difficulty')

class DifficultySchema(ma.Schema):
    tracks = fields.List(fields.Nested('TrackSchema', exclude=['difficulty']))

    class Meta:
        fields = ('id', 'difficulty', 'tracks')
        ordered = True

difficulty_schema = DifficultySchema()
difficulties_schema = DifficultySchema(many=True)