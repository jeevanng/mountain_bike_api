from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.region import Region, region_schema, regions_schema
from models.country import Country, countries_schema_exclude
from controllers.track_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Blueprint
regions_bp = Blueprint('regions', __name__,)

# Get region by region_name
# /<country_name>/region/<region_name> is the current route for below
@regions_bp.route('/<region_name>')
@jwt_required()
def get_region(country_name, region_name):
    # First query the database by the country_name that is entered into the route
    country_stmt = db.select(Country).filter_by(country_name=country_name)
    country = db.session.scalar(country_stmt)
    # If it does not exist in the database return error
    if not country:
        return {'error': f'Country {country_name} does not exist'}, 404

    # Query the database by country.id and <region_name>. Checking to see whether the region exists in the country 
    region_stmt = db.select(Region).filter_by(region_name=region_name, country_id=country.id)
    region = db.session.scalar(region_stmt)
    # If region does not exist within the country, show error message below
    if not region:
        return {'error': f'Region {region_name} does not exist in {country_name}'}, 404
    
    return region_schema.dump(region)

# Same as above but for post method
@regions_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_region(country_name):
    try: 
        # Country has to exist in the database before a region can be posted under that country.id
        country_stmt = db.select(Country).filter_by(country_name=country_name)
        country = db.session.scalar(country_stmt)
        if not country:
            return {'error': f'Country {country_name} does not exist'}, 404

        body_data = region_schema.load(request.get_json())

        regions = Region(
            region_name=body_data.get('region_name'),
            country_id=country.id
        )

        db.session.add(regions)
        db.session.commit()

        return region_schema.dump(regions), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': f"Region {regions.region_name}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required' }, 409
        
@regions_bp.route('/<region_name>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_region(country_name, region_name):
    # Query the database for the Country entity and filter by country_name=country_name
    country_stmt = db.select(Country).filter_by(country_name=country_name)
    country = db.session.scalar(country_stmt)
    if not country:
        return {'error': f'Country {country_name} does not exist'}, 404
    
    # Checking to see whether the region exists in the country. If it does not, return error message below
    stmt = db.select(Region).filter_by(country_id=country.id, region_name=region_name)
    region = db.session.scalar(stmt)
    if region:
        db.session.delete(region)
        db.session.commit()
        return {'message': f'Region {region.region_name} delete successfully'}
    else:
        return {'message': f'Region name of {region_name} was not found in {country_name}. Or region {region_name} does not exist.'}, 404
    