from config import configure_app
from flask import Flask, render_template
from models import Luggage, db
from routes import luggage
from sqlalchemy import create_engine
import flask.ext.whooshalchemy as whooshalchemy
from flask_moment import Moment
from datetime import datetime
from pytz import timezone

flask_app = Flask(__name__, template_folder='templates')


configure_app(flask_app)
db.init_app(flask_app)
moment = Moment(flask_app)

flask_app.register_blueprint(luggage)

whooshalchemy.whoosh_index(flask_app, Luggage)

@flask_app.teardown_appcontext
def close_db(error=None):
    """Closes the database again at the end of the request."""
    # Flask does .remove() automatically at the end of each HTTP request ("view" functions),
    # so the session is released by the current thread.
    pass





def datetimefilter(value, format='%I:%M %p'):
    tz = timezone('US/Eastern')
    dt = value
    local_dt = tz.localize(dt)
    local_dt.replace(hour=local_dt.hour + int(local_dt.utcoffset().total_seconds() / 3600))
    return local_dt.strftime(format)

flask_app.jinja_env.filters['datetimefilter'] = datetimefilter
