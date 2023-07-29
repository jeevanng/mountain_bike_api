from init import db, ma
from marshmallow import fields 

class MountainBike(db.Model):
    __tablename__ = "mountain_bikes"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)

    recommendations = db.relationship('Recommendation', back_populates='mountain_bike', cascade='all, delete')

class MountainBikeSchema(ma.Schema):
    id = fields.Integer()
    type = fields.String()
    description = fields.String()
    recommendations = fields.List(fields.Nested('RecommendationSchema', exclude=['mountain_bike']))

    fields = ('id', 'type', 'description', 'recommendations')
    ordered = True

mountain_bike_schema = MountainBikeSchema()
mountain_bikes_schema = MountainBikeSchema(many=True)
mountain_bikes_schema_exclude = MountainBikeSchema(many=True, exclude=['recommendations'])