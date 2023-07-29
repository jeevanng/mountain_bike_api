from init import db, ma
from marshmallow import fields 

class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)

    mountain_bike_id = db.Column(db.Integer, db.ForeignKey('mountain_bikes.id'), nullable=False)

    mountain_bike = db.relationship('MountainBike', back_populates='recommendations')

class RecommendationSchema(ma.Schema):
    mountain_bike = fields.Nested('MountainBikeSchema', exclude=['recommendations'])

    class Meta:
        fields = ('id', 'mountain_bike')