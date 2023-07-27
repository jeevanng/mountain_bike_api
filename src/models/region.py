from init import db, ma 
from marshmallow import fields 
from marshmallow.validate import Length, And, Regexp

class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String, nullable=False, unique=True)

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    country = db.relationship('Country', back_populates='regions')
    locations = db.relationship('Location', back_populates='region', cascade='all, delete')

class RegionSchema(ma.Schema):
    
    region = fields.String(required=True, validate=And(
        Length(min=2, error='Region must be at least 2 characters long'),
        Regexp("^[a-zA-Z ]+$", error="Only letters and spaces are allowed")))

    class Meta:
        fields = ('id', 'region', 'country')
        ordered = True

region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)
