#!/usr/bin/env python
#from config import configure_app
from flask import Flask, render_template
#from models import Luggage, db
#from routes import luggage
#from sqlalchemy import create_engine

app = Flask(__name__)

#configure_app(app)
#db.init_app(app)

@app.route('/')
def hello_world():
    #return 'Hello World!'
    # Uncomment the line below and remove the line above to render the index.html template
    return render_template('index.html')

#@app.teardown_appcontext
#def close_db(error=None):
#    """Closes the database again at the end of the request."""
    # Flask does .remove() automatically at the end of each HTTP request ("view" functions), 
    # so the session is released by the current thread.
#    pass
    
#engine = create_engine('sqlite:///./Luggage.db')
#db.metadata.create_all(bind=engine)      

if __name__ == '__main__':
    app.run(debug=True)
