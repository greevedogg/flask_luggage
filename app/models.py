from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime
from time import time
import flask.ext.whooshalchemy

db = SQLAlchemy()

class Luggage(db.Model):
    __tablename__ = 'luggage'
    __searchable__ = ['name','ticket']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ticket = db.Column(db.String(11))
    location = db.Column(db.String(11))
    bagCount = db.Column(db.Integer)
    loggedInBy = db.Column(db.String(3))#(db.Integer, db.ForeignKey('user.id'))
    modifiedBy = db.Column(db.String(3))
    lastModified = db.Column(db.DateTime)
    comments = db.Column(db.String(160))
    timeIn = db.Column(db.DateTime)
    #user = db.relationship('User',
                             #backref=db.backref('luggage', lazy='joined'))

    def __init__(self, name, ticket, location, bagCount, loggedInBy, comments, timeIn=None, lastModified=None):
        self.name = name.upper()
        self.ticket = ticket
        self.location = location
        self.bagCount = bagCount
        self.loggedInBy = loggedInBy.upper()
        self.comments = comments
        if timeIn is None:
            self.timeIn = datetime.utcnow()
            self.lastModified = datetime.utcnow()

    def __repr__(self):
        return '<Luggage %r>' % (self.name, self.ticket)

#if enable_search:
    #whooshalchemy.whoosh_index(app, Luggage)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userName = db.Column(db.String(30), unique=True)
#     pin = db.Column(db.String(10), unique=True)
#
#     def __init__(self, userName, pin):
#         self.userName = userName
#         self.pin = pin
#
#     def __repr__(self):
#         pass

class Archive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ticket = db.Column(db.String(11))
    location = db.Column(db.String(20))
    bagCount = db.Column(db.Integer)
    loggedInBy = db.Column(db.String(3))
    comments = db.Column(db.String(160))
    loggedOutBy = db.Column(db.String(3))
    modifiedBy = db.Column(db.String(3))
    lastModified = db.Column(db.DateTime)
    timeIn = db.Column(db.DateTime)
    timeOut = db.Column(db.DateTime)

    def __init__(self, name, ticket, location, bagCount, loggedInBy, timeIn, modifiedBy, lastModified, loggedOutBy=None, comments=None, timeOut=None):
        self.name = name
        self.ticket = ticket
        self.location = location
        self.bagCount = bagCount
        self.loggedInBy = loggedInBy.upper()
        self.loggedOutBy = loggedOutBy.upper()
        self.modifiedBy = modifiedBy.upper()
        self.lastModified = lastModified
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
        locations_selected = [item.location for item in query.all()]
        all_locations = {u'21a': u'21A', u'21b': u'21B', u'21c': u'21C'}

        locations_availability = {
            key: {'is_occupied': True if value in locations_selected else False, 'map_identifier': value}
            for key, value in all_locations.iteritems()}

        return locations_availability

#engine = create_engine('sqlite:///./Luggage.db')
#db.metadata.create_all(bind=engine)
