from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.region import Region, region_schema, regions_schema
from models.country import Country
from controllers.track_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

regions_bp = Blueprint('regions', __name__,)

@regions_bp.route('/<region_name>')
@jwt_required()
def get_locations_via_region(country_name, region_name):
    country_stmt = db.select(Country).filter_by(country=country_name)
    country = db.session.scalar(country_stmt)
    if not country:
        return {'error': f'Country {country_name} does not exist'}, 404

    region_stmt = db.select(Region).filter_by(region=region_name, country_id=country.id)
    region = db.session.scalar(region_stmt)
    if not region:
        return {'error': f'Region {region_name} does not exist in {country_name}'}, 404
    
    return region_schema.dump(region)