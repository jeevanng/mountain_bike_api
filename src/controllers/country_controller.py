from flask import Blueprint, request
from init import db 
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.track_controller import authorise_as_admin
from models.country import Country, country_schema, country_schema_exclude, countries_schema, countries_schema_exclude
from controllers.region_controller import regions_bp
from controllers.location_controller import locations_bp
from controllers.track_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Blueprints and registers for the routes
countries_bp = Blueprint('country', __name__, url_prefix='/country')
countries_bp.register_blueprint(regions_bp, url_prefix='/<country_name>/region')
countries_bp.register_blueprint(locations_bp, url_prefix='/<country_name>/region/<region_name>/location')

# Get all countries in the databse
@countries_bp.route('/')
@jwt_required()
def get_all_countries():
    # Select all the countries in the Country model and entity
    stmt = db.select(Country)
    countries = db.session.scalars(stmt)
    return countries_schema_exclude.dump(countries)

# Shows the regions belonging to the country_name 
@countries_bp.route('/<country_name>')
@jwt_required()
def get_one_country(country_name):
    # Query the Country model and filter by country_name=country_name
    stmt = db.select(Country).filter_by(country_name=country_name)
    country = db.session.scalar(stmt)
    if country:
        return country_schema.dump(country)
    else:
        return {'error': f'Country {country_name} does not exist'}, 404

# Create a new country
@countries_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def create_country():
    try:
        body_data = country_schema.load(request.get_json())
        
        countries = Country(
            country_name=body_data.get('country_name')  
        )

        db.session.add(countries)
        db.session.commit()

        return country_schema_exclude.dump(countries), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': f"Country {countries.country_name}' is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} is required' }, 409
    
# Delete country
@countries_bp.route('/<country_name>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_country(country_name):
        # Query the Country model and filter by country_name=country_name
        stmt = db.select(Country).filter_by(country_name=country_name)
        country = db.session.scalar(stmt)
        if country:
            db.session.delete(country)
            db.session.commit()
            return {'message': f'Country {country.country_name} was deleted successfully'}
        else:
            return {'message': f'Country name of {country_name} was not found'}, 404
    