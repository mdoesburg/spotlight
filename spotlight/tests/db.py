import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def resolve_dsn():
    return 'sqlite:///db.sqlite'


def engine(dsn=None):
    return create_engine(
        dsn or resolve_dsn(),
        echo=False
    )


def session(dsn=None):
    _dsn = dsn or resolve_dsn()
    factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine(_dsn)
    )
    _session = scoped_session(factory)
    Base.query = _session.query_property()

    return _session


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    password = Column(String(255))
    site_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )
