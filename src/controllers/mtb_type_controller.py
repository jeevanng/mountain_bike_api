from flask import Blueprint, request
from init import db 
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mtb_type import MountainBike, mountain_bike_schema, mountain_bikes_schema_exclude

mtb_types_bp = Blueprint('mtb_type', __name__, url_prefix='/mtb')

# Get all mountain bike types that exist in the database
@mtb_types_bp.route('/')
@jwt_required()
def get_all_mtb_types():
    # Select everything in the Mountain Bike entity 
    stmt = db.select(MountainBike)
    mtb_types = db.session.scalars(stmt)
    return mountain_bikes_schema_exclude.dump(mtb_types)

# Get the mountain bike type by id, and show the associated tracks for that mountain bike type. Show recommendations which includes 'tracks' field.
@mtb_types_bp.route('/<int:id>')
@jwt_required()
def get_track_by_mtb_type(id):
    # Query Mountain Bike model and filter where id=id
    stmt = db.select(MountainBike).filter_by(id=id)
    mtb_type = db.session.scalar(stmt)
    if mtb_type:
        return mountain_bike_schema.dump(mtb_type)
    else:
        return {'error': f'Mountain Bike Type not found with id {id}'}, 404