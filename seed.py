"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import User, Message, Follows


db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

demoUser = User.signup(username='demo-user', password='password', email='demo@gmail.com', image_url=User.image_url.default.arg)

db.session.add(demoUser)
db.session.commit()

for id in range(1, 10):
    print(id)
    demoFollows = Follows(user_being_followed_id=id, user_following_id=301)
    db.session.add(demoFollows)

db.session.commit()     


