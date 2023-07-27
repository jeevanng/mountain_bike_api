from init import db, ma 
from marshmallow import fields 
from marshmallow.validate import Length, And, Regexp

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False, unique=True)

    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

    region = db.relationship('Region', back_populates='locations')

class LocationSchema(ma.Schema):

     location = fields.String(required=True, validate=And(
        Length(min=2, error='Location must be at least 2 characters long'),
        Regexp("^[a-zA-Z ]+$", error="Only letters and spaces are allowed")))
     
     class Meta:
          fields = ('id', 'location', 'region')
          ordered = True

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)