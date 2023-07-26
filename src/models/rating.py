from init import db, ma 
from marshmallow import fields

class Rating(db.Model):
    __tablename__= "ratings"

    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False, unique=True)

    tracks = db.relationship('Track', back_populates='rating')

class RatingSchema(ma.Schema):
    tracks = fields.List(fields.Nested('TrackSchema', exclude=['rating']))

    class Meta:
        fields = ('id', 'stars', 'tracks')
        ordered = True

star_schema = RatingSchema()
stars_schema = RatingSchema(many=True)
stars_schema_exclude = RatingSchema(many=True, exclude=['tracks'])