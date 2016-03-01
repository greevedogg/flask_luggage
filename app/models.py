from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    loggedInBy = db.Column(db.String(2))
    timeIn = db.Column(db.DateTime)

    def __init__(self, name, ticket, location, bagCount, loggedInBy, timeIn=None):
        self.name = name
        self.ticket = ticket
        self.location = location
        self.bagCount = bagCount
        self.loggedInBy = loggedInBy
        if timeIn is None:
            self.timeIn = datetime.utcnow()

    def __repr__(self):
        return '<Luggage %r>' % (self.name, self.ticket)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(30), unique=True)
    pin = db.Column(db.String(10), unique=True)

    def __init__(self, userName, pin):
        self.userName = userName
        self.pin = pin

    def __repr__(self):
        pass

class archive(db.Model):

    name = db.Column(db.String(30))
    ticket = db.Column(db.String(11))
    location = db.Column(db.String(20))
    bagCount = db.Column(db.Integer)
    loggedInBy = db.Column(db.String(3))
    comments = db.Column(db.String(160))
    loggedOutBy = db.Column(db.String(3))
    id = db.Column(db.Integer, primary_key=True)
    timeIn = db.Column(db.DateTime)
    timeOut = db.Column(db.DateTime)

    def __init__(self, name, ticket, location, bagCount, loggedInBy, comments, loggedOutBy, timeIn=None, timeOut=None):
        self.name = name
        self.ticket = ticket
        self.location = location
        self.bagCount = bagCount
        self.loggedInBy = loggedInBy
        self.comments = comments
        self.loggedOutBy = loggedOutBy
        self.timeIn = datetime.datetime
        self.timeOut = datetime.utcnow()

    def __repr__(self):
        pass
