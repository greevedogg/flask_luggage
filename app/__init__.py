# from sqlalchemy import create_engine
# from pytz import timezone
# import tzlocal
from config import configure_app
from flask import Flask, render_template
from models import Luggage, db, Archive
from routes import luggage
import flask.ext.whooshalchemy as whooshalchemy
from flask_moment import Moment
from datetime import datetime
import pytz
from flask_sslify import SSLify
import json
import string
import os

flask_app = Flask(__name__, template_folder='templates')

SSLify(flask_app)

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

# TODO: move filters and helpers to their own file
def datetimefilter(value, format="%I:%M %p"):
    tz = pytz.timezone('US/Eastern') # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

@flask_app.context_processor
def utility_processor():
    def currentyear():
        return datetime.now().year

    def locations(selected_locations):
        selected_locations = json.loads(selected_locations) if selected_locations else dict()
        locations_filtered = {key: value for key, value in selected_locations.iteritems() if value}
        keys = []

        if locations_filtered:
            keys = locations_filtered.keys()
            keys.sort(key=string.lower)

        return ' '.join(keys)

    def is_production():
        return config.PRODUCTION in os.getenv('FLAKS_CONFIGURATION', '')

    return dict(current_year=currentyear, locations=locations, is_production=is_production)

flask_app.jinja_env.filters['datetimefilter'] = datetimefilter
