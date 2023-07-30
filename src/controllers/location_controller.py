from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.location import Location, location_schema
from controllers.track_controller import authorise_as_admin
from models.country import Country
from models.region import Region

locations_bp = Blueprint('locations', __name__,)

# Get the tracks associated with the location 
@locations_bp.route('/<location_name>')
@jwt_required()
def get_location(country_name, region_name, location_name):
    # Check to see whether the country exists in the databse
    country_stmt = db.select(Country).filter_by(country_name=country_name)
    country = db.session.scalar(country_stmt)
    if not country:
        return {'error': f'Country {country_name} does not exist'}, 404
    
    # Check to see whether the region is within the country stated
    region_stmt = db.select(Region).filter_by(region_name=region_name, country_id=country.id)
    region = db.session.scalar(region_stmt)
    if not region:
        return {'error': f'Region {region_name} does not exist in {country_name}'}, 404
    
    # If location exists in the region, return schema. Otherwise show error message below
    location_stmt = db.select(Location).filter_by(region_id=region.id, location_name=location_name)
    location = db.session.scalar(location_stmt)
    if not location:
        return {'error': f'Location {location_name} does not exist in {region_name}'}, 404
    
    return location_schema.dump(location)

@locations_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_location(country_name, region_name):
    try:
        country_stmt = db.select(Country).filter_by(country_name=country_name)
        country = db.session.scalar(country_stmt)
        if not country:
            return {'error': f'Country {country_name} does not exist'}, 404
        
        region_stmt = db.select(Region).filter_by(region_name=region_name, country_id=country.id)
        region = db.session.scalar(region_stmt)
        if not region: 
            return {'error': f'Region {region_name} does not exist in {country_name}'}, 404
        
        body_data = location_schema.load(request.get_json())

        locations = Location(
            location_name=body_data.get('location_name'),
            latitude=body_data.get('latitude'),
            longitude=body_data.get('longitude'),
            region_id=region.id
        )

        db.session.add(locations)
        db.session.commit()

        return location_schema.dump(locations), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': f"Location {locations.location_name}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required' }, 409
    
# Same as above. Checks to see whether country exists. Whether the region exists in the country, and then whether the location exists 
# in that region. If any of those are not true, return error messages. 
@locations_bp.route('/<location_name>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_location(country_name, region_name, location_name):
    country_stmt = db.select(Country).filter_by(country_name=country_name)
    country = db.session.scalar(country_stmt)
    if not country:
        return {'error': f'Country {country_name} does not exist'}, 404
        
    region_stmt = db.select(Region).filter_by(region_name=region_name, country_id=country.id)
    region = db.session.scalar(region_stmt)
    if not region: 
        return {'error': f'Region {region_name} does not exist in {country_name}'}, 404
        
    stmt = db.select(Location).filter_by(region_id=region.id, location_name=location_name)
    location = db.session.scalar(stmt)
    if location:
        db.session.delete(location)
        db.session.commit()
        return {'message': f'Location {location.location_name} deleted successfully'}
    else:
        return {'message': f'Location name of {location_name} was not found in {region_name}. Or location {location_name} does not exist.'}, 404
    

        