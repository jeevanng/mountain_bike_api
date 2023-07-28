from flask import Flask 
from init import db, ma, bcrypt, jwt 
import os 
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.track_controller import tracks_bp
from controllers.difficulty_controller import difficulties_bp
from controllers.rating_controller import ratings_bp
from controllers.country_controller import countries_bp
from marshmallow.exceptions import ValidationError

def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tracks_bp)
    app.register_blueprint(difficulties_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(countries_bp)

    return app