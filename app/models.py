from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Luggage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    ticket = db.Column(db.String(11))
    location = db.Column(db.String(11))
    bagCount = db.Column(db.Integer)
    loggedIn = db.Column(db.String(30), db.ForeignKey('user.id'))
    timeIn = time(now(%H:%M))
    
    def __init__(self, name, ticket, location, bagCount, loggedIn, timeIn):
        self.name = name
        self.ticket = ticket
        self.location = location
        self.bagCount = bagCount
        self.loggedIn = loggedIn
        self.timeIn = timeIn
    
    def __repr__(self):
        ??????????????
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(30), unique=True)
    pin = db.Column(db.String(10), unique=True)
    
    def __intit__(self, userName, pin):
        self.userName = userName
        self.pin = pin
        
    def __repr__(self):
        ??????????????????
    
