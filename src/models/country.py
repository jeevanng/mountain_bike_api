from init import db, ma 
from marshmallow import fields 
from marshmallow.validate import Length, And, Regexp

class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String, nullable=False, unique=True)

    regions = db.relationship('Region', back_populates='country', cascade='all, delete')

class CountrySchema(ma.Schema):
    regions = fields.List(fields.Nested('RegionSchema', exclude=['country', 'locations']))
    country_name = fields.String(required=True, validate=And(
        Length(min=2, error='Country must be at least 2 characters long'),
        Regexp("^[a-zA-Z-]+$", error="Only letters and - are allowed. Please use - instead of space")))

    class Meta:
        fields = ('id', 'country_name', 'regions')
        ordered = True

country_schema_exclude = CountrySchema(exclude=['regions'])
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
countries_schema_exclude = CountrySchema(many=True, exclude=['regions'])
