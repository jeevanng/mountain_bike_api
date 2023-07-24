from flask import Blueprint 
from init import db, bcrypt 
from models.user import User
from models.track import Track
from models.comment import Comment
from models.difficulty import Difficulty
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

    tracks = [
        Track(
            name="Fall Line",
            duration=datetime.time(hour=0, minute=3, second=22),
            description="Rocky, chunky and rutted out downhill with lots of flow",
            distance=765,
            climb=0,
            descent=-102,
            difficulty=difficulties[0],
            user=users[0]
        ),
        Track(
            name="Wombat",
            duration=datetime.time(hour=0, minute=6, second=22),
            description="Jump on the roller coaster express and send it down these manicured flowly berms. Hard packed dirt for ultimate smoothness",
            distance=1700,
            climb=5,
            descent=-91,
            difficulty=difficulties[1],
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
            user=users[0]
        ),
    ]

    db.session.add_all(tracks)

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
