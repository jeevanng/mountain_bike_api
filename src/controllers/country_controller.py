from flask import Blueprint, request
from init import db 
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.track_controller import authorise_as_admin
from models.country import Country, country_schema, country_schema_exclude, countries_schema, countries_schema_exclude
from controllers.region_controller import regions_bp
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

countries_bp = Blueprint('country', __name__, url_prefix='/country')
countries_bp.register_blueprint(regions_bp, url_prefix='/<country_name>/region')

@countries_bp.route('/')
@jwt_required()
def get_all_countries():
    stmt = db.select(Country)
    countries = db.session.scalars(stmt)
    return countries_schema_exclude.dump(countries)

@countries_bp.route('/<country_name>')
@jwt_required()
def get_one_country(country_name):
    stmt = db.select(Country).filter_by(country=country_name)
    country = db.session.scalar(stmt)
    if country:
        return country_schema.dump(country)
    else:
        return {'error': f'Country {country_name} does not exist'}, 404
    