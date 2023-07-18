from flask import Blueprint, request
from init import db
from models.track import Track, track_schema, tracks_schema

tracks_bp = Blueprint('tracks', __name__, url_prefix='/tracks')

@tracks_bp.route('/')
def get_all_tracks():
    stmt = db.select(Track)
    tracks = db.session.scalars(stmt)
    return tracks_schema.dump(tracks)

