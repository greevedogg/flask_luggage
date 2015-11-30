from app import flask_app
from app.models import db, Luggage, User

def create_users_and_luggage(db):
    user1 = User('user1', 1234)
    user2 = User('user2', 5678)

    luggage1 = Luggage('luggage1', 'ticket1', 'location1', 3, user1)
    luggage2 = Luggage('luggage2', 'ticket2', 'location2', 1, user2)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(luggage1)
    db.session.add(luggage2)

    db.session.commit()

with flask_app.app_context():
    db.drop_all()
    db.create_all()

    create_users_and_luggage(db)
