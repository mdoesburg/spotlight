import unittest

from spotlight.validator import Validator
from spotlight.tests.db import Base, User, engine, session


class ValidatorTest(unittest.TestCase):
    _session = None

    @classmethod
    def setUpClass(cls):
        cls._setUpDatabase()
        cls.validator = Validator()
        cls.validator_with_session = Validator(cls._session)

    @classmethod
    def _setUpDatabase(cls):
        _engine = engine()

        Base.metadata.drop_all(_engine)
        Base.metadata.create_all(_engine)

        cls._session = session()
        cls._create_test_users()

    @classmethod
    def _create_test_users(cls):
        users = [
            User(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="555-539-4123",
                password="this.is.a.test.password",
                site_id=1
            ),
            User(
                first_name="Jane",
                last_name="Doe",
                email="jane.doe@example.com",
                phone="555-540-5244",
                password="this.is.a.test.password",
                site_id=2
            )
        ]
        cls._session.add_all(users)
        cls._session.commit()

    @classmethod
    def tearDownClass(cls):
        cls._session.close()
