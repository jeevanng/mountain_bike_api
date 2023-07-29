from init import db, ma
from marshmallow import fields 

class MountainBike(db.Model):
    __tablename__ = "mountain_bikes"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)

class MountainBikeSchema(ma.Schema):
    fields = ('id', 'name', 'description')
    ordered = True

mountain_bike_schema = MountainBikeSchema()
mountain_bikes_schema = MountainBikeSchema(many=True)