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
    loggedIn = db.Column(db.Integer, db.ForeignKey('user.id'))
    timeIn = db.Column(db.DateTime)
    user = db.relationship('User',
                             backref=db.backref('luggage', lazy='joined'))

    def __init__(self, name, ticket, location, bagCount, user, timeIn=None):
        self.name = name
        self.ticket = ticket
        self.location = location
        self.bagCount = bagCount
        self.user = user
        if timeIn is None:
            self.timeIn = datetime.utcnow()

    def __repr__(self):
        return '<Luggage %r>' % (self.name, self.ticket)

#if enable_search:
    #whooshalchemy.whoosh_index(app, Luggage)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(30), unique=True)
    pin = db.Column(db.String(10), unique=True)

    def __init__(self, userName, pin):
        self.userName = userName
        self.pin = pin

    def __repr__(self):
        pass


#engine = create_engine('sqlite:///./Luggage.db')
#db.metadata.create_all(bind=engine)
