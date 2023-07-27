from init import db, ma 
from marshmallow import fields 
from marshmallow.validate import Length, And, Regexp

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

    region = db.relationship('Region', back_populates='locations')

class LocationSchema(ma.Schema):
    region = fields.Nested('RegionSchema', exclude=['locations'])

    location = fields.String(required=True, validate=And(
        Length(min=2, error='Location must be at least 2 characters long'),
        Regexp("^[a-zA-Z ]+$", error="Only letters and spaces are allowed")))
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
     
    class Meta:
        fields = ('id', 'location', 'latitude', 'longitude', 'region')
        ordered = True

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)