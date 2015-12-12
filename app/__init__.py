from config import configure_app
from flask import Flask, render_template
from models import Luggage, db
from routes import luggage
from sqlalchemy import create_engine

flask_app = Flask(__name__, template_folder='templates')

configure_app(flask_app)
db.init_app(flask_app)

flask_app.register_blueprint(luggage, url_prefix='/luggage')

@flask_app.teardown_appcontext
def close_db(error=None):
    """Closes the database again at the end of the request."""
    # Flask does .remove() automatically at the end of each HTTP request ("view" functions), 
    # so the session is released by the current thread.
    pass
    
engine = create_engine('sqlite:///./Luggage.db')
db.metadata.create_all(bind=engine)      