from config import configure_app
from flask import Flask, render_template
from models import Luggage, db, archive
from routes import luggage
from sqlalchemy import create_engine
import flask.ext.whooshalchemy as whooshalchemy
from flask_moment import Moment
from datetime import datetime
import pytz
from pytz import timezone
import tzlocal

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

def datetimefilter(value, format="%I:%M %p"):
    tz = pytz.timezone('US/Eastern') # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

flask_app.jinja_env.filters['datetimefilter'] = datetimefilter
