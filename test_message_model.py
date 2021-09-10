import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable to use a different database for tests

os.environ['DATABASE_URL'] = 'postgresql:///warbler-test'

from app import app

db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 1000
        u = User.signup('testing', 'testing@test.com', 'password', None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        '''Does basic model work?'''

        m = Message(text='test123', user_id=self.uid)

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, 'test123')

    def test_message_likes(self):
        m1 = Message(text='test123', user_id=self.uid)

        m2 = Message(text='hello', user_id=self.uid)

        u = User.signup('testing2', 'testing2@test.com', 'password2', None)
        uid = 1001
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)