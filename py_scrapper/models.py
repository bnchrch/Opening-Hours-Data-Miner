from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import random

import settings
from sqlalchemy.orm import sessionmaker


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class PlaceSearchHistory(DeclarativeBase):
    """Sqlalchemy place search history model"""
    __tablename__ = "place_search_history"

    id = Column(Integer, primary_key=True)
    api_key = Column('api_key', String)
    lat = Column('lat', Numeric, nullable=False)
    long = Column('long', Numeric, nullable=False)
    radius = Column('radius', Integer, nullable=False)
    date = Column('date', DateTime, nullable=True)


class PlaceDetails(DeclarativeBase):
    """Sqlalchemy place details model"""
    __tablename__ = "place_details"

    place_id = Column(String, primary_key=True)
    name = Column('name', String)
    #place_search_id = Column('place_search_id', Integer, ForeignKey("place_search_history.id"))
    address = Column('address', String, nullable=True)
    phone_number = Column('phone_number', String, nullable=True)
    url = Column('url', String, nullable=True)
    rating = Column('rating', Numeric, nullable=True)
    lat = Column('lat', Numeric)
    long = Column('long', Numeric)


class PlaceHours(DeclarativeBase):
    """Sqlalchemy place hours model"""
    __tablename__ = "place_hours"

    place_id = Column(String, ForeignKey("place_details.place_id"))
    day = Column('day', Integer)
    open_time = Column('open_time', Integer, nullable=True)
    close_time = Column('close_time', Integer, nullable=True)
    __table_args__ = (PrimaryKeyConstraint('place_id', 'day', name='place_hours_pk'),)


class PlaceTypes(DeclarativeBase):
    """Sqlalchemy place types model"""
    __tablename__ = "place_types"

    place_id = Column(String, ForeignKey("place_details.place_id"))
    type_title = Column('type_title', String)
    __table_args__ = (PrimaryKeyConstraint('place_id', 'type_title', name='place_types_pk'),)


class PlacesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)
        session = self.Session()
        self.values =[str(value[0]) for value in session.query(PlaceTypes.type_title).distinct()]
        session.close()

    def process_details(self, detail_json):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        place_details = PlaceDetails(place_id=detail_json.get('place_id', None),
                                     name=detail_json.get('name', None),
                                     address=detail_json.get('formatted_address', None),
                                     phone_number=detail_json.get('formatted_number', None),
                                     url=detail_json.get('url', None),
                                     rating=detail_json.get('rating', None),
                                     lat=detail_json['geometry']['location']['lat'],
                                     long=detail_json['geometry']['location']['lng'])
        type_objects = []
        for type_title in detail_json.get('types', []):
            type_objects.append(PlaceTypes(place_id=detail_json.get('place_id', None),
                                           type_title=type_title))

        opening_hours = detail_json.get('opening_hours', {}).get('periods', {})
        hours_objects = []
        for period in opening_hours:
            close_time = period.get('close', None)
            if close_time:
                close_time = close_time['time']
            hours_objects.append(PlaceHours(place_id=detail_json.get('place_id', None),
                                           day=period['open']['day'],
                                           open_time=period['open']['time'],
                                           close_time=close_time
                                           ))

        try:
            print 'trying'
            session.add(place_details)
            session.commit()

            for type in type_objects:
                session.add(type)
            for hours in hours_objects:
                session.add(hours)
            session.commit()
        except:
            print 'error!'
            session.rollback()
            raise
        finally:
            print 'closed session'
            session.close()

        return detail_json

    def get_details_by_id(self, place_id):
        session = self.Session()
        q = session.query(PlaceDetails)
        place = q.filter_by(place_id=place_id).first()
        session.close()
        return place

    def get_type_string_for_query(self, num=5):
        return "|".join(random.sample(self.values, num))


