# from sqlalchemy import create_engine
# from time import time
# import flask.ext.whooshalchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import json

db = SQLAlchemy()


class Luggage(db.Model):
    __tablename__ = 'luggage'
    __searchable__ = ['name','ticket']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ticket = db.Column(db.String(11))
    location = db.Column(db.String(255))
    bagCount = db.Column(db.Integer)
    loggedInBy = db.Column(db.String(3))#(db.Integer, db.ForeignKey('user.id'))
    modifiedBy = db.Column(db.String(3))
    lastModified = db.Column(db.DateTime)
    comments = db.Column(db.String(160))
    timeIn = db.Column(db.DateTime, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))

    def __init__(self, name, ticket, location, bagCount, loggedInBy, comments, hotel_id, timeIn=None, lastModified=None):
        self.name = name.upper()
        self.ticket = ticket
        self.location = location.upper()
        self.bagCount = bagCount
        self.loggedInBy = loggedInBy.upper()
        self.comments = comments
        self.hotel_id = hotel_id
        if timeIn is None:
            self.timeIn = datetime.utcnow()
            self.lastModified = datetime.utcnow()

    def __repr__(self):
        return '<Luggage %r>' % (self.name, self.ticket)

#if enable_search:
    #whooshalchemy.whoosh_index(app, Luggage)


class User(db.Model):
    """An admin user capable of access specific hotel.

    :param str username: the name for specific user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    authenticated = db.Column(db.Boolean, default=False)
    # foreign key
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    # define relationship
    hotel = db.relationship('Hotel', uselist=False, backref='users')
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id field."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image = db.Column(db.String(150))
    luggages = db.relationship("Luggage", backref="hotel")
    archives = db.relationship("Archive", backref="hotel")


class Archive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ticket = db.Column(db.String(11))
    location = db.Column(db.String(255))
    bagCount = db.Column(db.Integer)
    loggedInBy = db.Column(db.String(3))
    comments = db.Column(db.String(160))
    loggedOutBy = db.Column(db.String(3))
    modifiedBy = db.Column(db.String(3))
    lastModified = db.Column(db.DateTime)
    timeIn = db.Column(db.DateTime, nullable=False)
    timeOut = db.Column(db.DateTime, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    
    def __init__(self, name, ticket, location, bagCount, loggedInBy, timeIn, modifiedBy, lastModified, hotel_id, loggedOutBy=None, comments=None, timeOut=None):
        self.name = name.upper()
        self.ticket = ticket
        self.location = location.upper()
        self.bagCount = bagCount
        self.loggedInBy = loggedInBy.upper()
        self.loggedOutBy = loggedOutBy.upper()
        self.modifiedBy = modifiedBy.upper() if modifiedBy else modifiedBy
        self.lastModified = lastModified
        self.hotel_id = hotel_id
        self.comments = comments
        self.timeIn = timeIn
        self.timeOut = datetime.utcnow()

    def __repr__(self):
        pass


class Location(object):
    def __init(self):
        pass

    def availability(self):
        query = db.session.query(Luggage.location.distinct().label('location'))
        locations_selected = [Counter(json.loads(item.location)) for item in query.all() if item.location]
        all_locations = {
            u'21a': u'21A',
            u'21b': u'21B',
            u'21c': u'21C',
            u'22a': u'22A',
            u'22b': u'22B',
            u'22c': u'22C',
            u'14a': u'14A',
            u'14b': u'14B',
            u'14c': u'14C',
            u'transfer': u'TRANS.',
            u'cart_front': u'CART',
        }

        counter = Counter()

        for location in locations_selected:
            counter += location

        locations_availability = {
            key: {
                'is_occupied': True if value in counter else False,
                'map_identifier': value,
                'amount': counter[value] if value in counter else 0
            }
            for key, value in all_locations.iteritems()}

        return locations_availability

#engine = create_engine('sqlite:///./Luggage.db')
#db.metadata.create_all(bind=engine)
