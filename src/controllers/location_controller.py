from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.location import Location, location_schema
from models.country import Country
from models.region import Region

locations_bp = Blueprint('locations', __name__,)

@locations_bp.route('/<location_name>')
@jwt_required()
def get_location(country_name, region_name, location_name):
    country_stmt = db.select(Country).filter_by(country_name=country_name)
    country = db.session.scalar(country_stmt)
    if not country:
        return {'error': f'Country {country_name} does not exist'}, 404
    
    region_stmt = db.select(Region).filter_by(region_name=region_name, country_id=country.id)
    region = db.session.scalar(region_stmt)
    if not region:
        return {'error': f'Region {region_name} does not exist in {country_name}'}, 404
    
    location_stmt = db.select(Location).filter_by(region_id=region.id, location_name=location_name)
    location = db.session.scalar(location_stmt)
    if not location:
        return {'error': f'Location {location_name} does not exist in {region_name}'}, 404
    
    return location_schema.dump(location)
