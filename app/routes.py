import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request, flash
from forms import LuggageForm
from flask.ext.wtf import Form

app = Flask(__name__) 
 
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'luggage.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('LUGGAGE_SETTINGS', silent=True)

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource(schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database')

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

   
@app.route('/luggage')
def luggage():
  form = LuggageForm()
  return render_template('luggage.html', form=form)
  
@app.route('/luggage', methods=['GET', 'POST'])
def luggage():
  form = LuggageForm()
 
  if request.method == 'POST':
   if form.validate() == False:
      flash('All fields are required.')
      return render_template('luggage.html', form=form)
   else:
    return 'Entry Submitted to Luggage Log.'
 
  elif request.method == 'GET':
    return render_template('luggage.html', form=form)  
  
