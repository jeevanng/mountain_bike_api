from flask import Blueprint 
from init import db, bcrypt 
from models.user import User
from models.track import Track
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
            email="admin@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        User(
            name="User1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    tracks = [
        Track(
            name="Fall Line",
            duration=datetime.time(hour=0, minute=3, second=22),
            description="Rocky, chunky and rutted out downhill with lots of flow",
            distance=765,
            climb=0,
            descent=102,
            user=users[0]
        ),
        Track(
            name="Wombat",
            duration=datetime.time(hour=0, minute=6, second=22),
            description="Smooth flowy manicured berms to provide a roller coaster like experience",
            distance=1700,
            climb=5,
            descent=-91,
            user=users[0]
        ),
        Track(
            name="Crusher",
            duration=datetime.time(hour=0, minute=9, second=24),
            description="Beware the first feature, for thou shall crush",
            distance=1300,
            climb=11,
            descent=-114,
            user=users[0]
        ),
    ]

    db.session.add_all(tracks)

    db.session.commit()

    print("Tables Seeded")
