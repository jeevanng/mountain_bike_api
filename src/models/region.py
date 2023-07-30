from init import db, ma 
from marshmallow import fields 
from marshmallow.validate import Length, And, Regexp

class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String, nullable=False, unique=True)

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    country = db.relationship('Country', back_populates='regions')
    # When a region is deleted, delete all the locations linked to that region
    locations = db.relationship('Location', back_populates='region', cascade='all, delete')

class RegionSchema(ma.Schema):
    country = fields.Nested('CountrySchema', exclude=['regions'])
    locations = fields.List(fields.Nested('LocationSchema', exclude=['region']))
    region_name = fields.String(required=True, validate=And(
        Length(min=2, error='Region must be at least 2 characters long'),
        Regexp("^[a-zA-Z-]+$", error="Only letters and - are allowed. Please use - instead of space")))

    class Meta:
        fields = ('id', 'region_name', 'country', 'locations')
        ordered = True

region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)
