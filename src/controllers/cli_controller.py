from flask import Blueprint 
from init import db, bcrypt 
from models.user import User
from models.track import Track
from models.comment import Comment
from models.difficulty import Difficulty
from models.rating import Rating
from models.country import Country
from models.region import Region
from models.location import Location
from models.mtb_type import MountainBike
from models.recommendation import Recommendation
from datetime import date
import datetime


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print("Tables Dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name="Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        User(
            name="Admin2",
            email="admin2@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        User(
            name="User1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name="User2",
            email="user2@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    countries = [
        Country(
            country_name="Australia"
        ),
        Country(
            country_name="New-Zealand"
        ),
        Country(
            country_name="Peru"
        ),
        Country(
            country_name="Canada"
        ),
        Country(
            country_name="Italy"
        ),
    ]

    db.session.add_all(countries)

    regions = [
        Region(
            region_name="Victoria",
            country=countries[0]
        ),
        Region(
            region_name="Tasmania",
            country=countries[0]
        ),
        Region(
            region_name="Cusco",
            country=countries[2]
        ),
        Region(
            region_name="British-Columbia",
            country=countries[3]
        ),
        Region(
            region_name="Ontario",
            country=countries[3]
        ),
        Region(
            region_name="Alberta",
            country=countries[3]
        ),
    ]

    db.session.add_all(regions)

    locations = [
        Location(
            location_name="Lysterfield",
            latitude=-37.933109,
            longitude=145.303299,
            region=regions[0]
        ),
        Location(
            location_name="Bright",
            latitude=-36.730194,
            longitude=146.960896,
            region=regions[0]
        ),
        Location(
            location_name="Plenty-Gorge",
            latitude=-37.020100,
            longitude=144.964600,
            region=regions[0]
        ),
        Location(
            location_name="Whistler",
            latitude=50.116322,
            longitude=-122.957359,
            region=regions[3]
        ),
        Location(
            location_name="Maydena",
            latitude=-42.75584,
            longitude=146.62636,
            region=regions[1]
        ),
        Location(
            location_name="Turkey-Point",
            latitude=42.680986,
            longitude=-80.332176,
            region=regions[4]
        ),
    ]

    db.session.add_all(locations)

    ratings = [
        Rating(
            stars=1
        ),
        Rating(
            stars=2
        ),
        Rating(
            stars=3
        ),
        Rating(
            stars=4
        ),
        Rating(
            stars=5
        ),
    ]

    db.session.add_all(ratings)

    difficulties = [
         Difficulty(
            difficulty_name="Green"
        ),
        Difficulty(
            difficulty_name="Blue"
        ),
        Difficulty(
            difficulty_name="Red"
        ),
        Difficulty(
            difficulty_name="Black"
        ),
        Difficulty(
            difficulty_name="Double Black"
        ),
        Difficulty(
            difficulty_name="Proline"
        ),
    ]

    db.session.add_all(difficulties)

    mountain_bike_types = [
        MountainBike(
            type="Hard-Tail",
            description="Suspension on the front fork, not rear"    
        ),
        MountainBike(
            type="Cross-Country",
            description="Low weight, tailored for back country"    
        ),
        MountainBike(
            type="Trail",
            description="Front fork travel between 120-150mm"    
        ),
        MountainBike(
            type="Enduro",
            description="Less versatile than cross-country and trail bikes. Beefier for downhill sections. Travel greater than 150mm."    
        ),
        MountainBike(
            type="Downhill",
            description="Maximum suspension. Front fork 200mm plus. Not good for riding uphill."    
        ),
    ]

    db.session.add_all(mountain_bike_types)

    tracks = [
        Track(
            name="Fall Line",
            duration=datetime.time(hour=0, minute=3, second=22),
            description="Rocky, chunky and rutted out downhill with lots of flow",
            distance=765,
            climb=0,
            descent=-102,
            difficulty=difficulties[0],
            rating=ratings[1],
            location=locations[0],
            user=users[0]
        ),
        Track(
            name="Wombat",
            duration=datetime.time(hour=0, minute=15, second=29),
            description="Jump on the roller coaster express and send it down these manicured flowly berms. Hard packed dirt for ultimate smoothness",
            distance=1700,
            climb=5,
            descent=-91,
            difficulty=difficulties[1],
            rating=ratings[3],
            location=locations[0],
            user=users[0]
        ),
        Track(
            name="Toilet Bowl",
            duration=datetime.time(hour=1, minute=16, second=24),
            description="Don't get FLUSHED!",
            distance=4000,
            climb=11,
            descent=-500,
            difficulty=difficulties[4],
            rating=ratings[4],
            location=locations[3],
            user=users[0]
        ),
        Track(
            name="Rock Garden",
            duration=datetime.time(hour=0, minute=32, second=24),
            description="Bumpy technical rock garden.",
            distance=1300,
            climb=324,
            descent=0,
            difficulty=difficulties[3],
            rating=ratings[2],
            location=locations[3],
            user=users[0]
        ),
        Track(
            name="Crusher",
            duration=datetime.time(hour=0, minute=9, second=24),
            description="Beware the first feature, for thou shall get CRUSHEDDDD",
            distance=1300,
            climb=11,
            descent=-114,
            difficulty=difficulties[2],
            rating=ratings[4],
            location=locations[1],
            user=users[0]
        ),
        Track(
            name="Underground Tunnel",
            duration=datetime.time(hour=0, minute=54, second=24),
            description="Dark",
            distance=1034,
            climb=3,
            descent=-5,
            difficulty=difficulties[2],
            rating=ratings[4],
            location=locations[2],
            user=users[1]
        ),
    ]

    db.session.add_all(tracks)

    recommendations = [
        Recommendation(
            mountain_bike=mountain_bike_types[0],
            track=tracks[1]
        ),
        Recommendation(
            mountain_bike=mountain_bike_types[1],
            track=tracks[1]
        ),
        Recommendation(
            mountain_bike=mountain_bike_types[2],
            track=tracks[0]
        ),
        Recommendation(
            mountain_bike=mountain_bike_types[3],
            track=tracks[0]
        ),
        Recommendation(
            mountain_bike=mountain_bike_types[4],
            track=tracks[4]
        ),
        Recommendation(
            mountain_bike=mountain_bike_types[3],
            track=tracks[4]
        ),
        Recommendation(
            mountain_bike=mountain_bike_types[2],
            track=tracks[4]
        ),
    ]
    
    db.session.add_all(recommendations)

    comments = [
        Comment(
            message="Tree has fallen over track, near the start. Avoid until further notice.",
            date=date.today(),
            user=users[0],
            track=tracks[0]
        ),
        Comment(
            message="Unreal track, one of my favourites.",
            date=date.today(),
            user=users[1],
            track=tracks[1]
        ),
        Comment(
            message="Super chunky today, conditions are rough.",
            date=date.today(),
            user=users[1],
            track=tracks[2]
        ),
        Comment(
            message="Just sent this track today, absolutely bonkers!",
            date=date.today(),
            user=users[1],
            track=tracks[2]
        ),
    ]

    db.session.add_all(comments)

    db.session.commit()

    print("Tables Seeded")
