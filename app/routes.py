# import os
# from sqlite3 import dbapi2 as sqlite3
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import Form
# from wtforms import validators
# import flask.ext.whooshalchemy
from flask import Blueprint, g, redirect, render_template, request, flash
from helpers import url_for
from forms import LuggageForm, SearchForm, LoginForm
from models import Luggage, db, Archive, Hotel, User
from sqlalchemy import exc, or_
from config import MAX_SEARCH_RESULTS
import re
from datetime import datetime, timedelta
import os
from whoosh.index import LockError
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import HotelForm
from werkzeug.utils import secure_filename
from app.config import UPLOAD_FOLDER
from flask import send_from_directory
from app.stats import get_first_and_last_stores, get_luggage_time, count_stores,\
    count_stores_by_hour
from collections import OrderedDict

luggage = Blueprint('luggage', __name__, template_folder='templates')


@luggage.before_request
def before_request():
    g.search_form = SearchForm(request.form)


@luggage.route('/luggage', methods=['GET', 'POST'])
@login_required
def create_luggage():
    form = LuggageForm(request.form)

    items = [item for item in Luggage.query.order_by(Luggage.timeIn.desc()).filter_by(hotel_id=current_user.hotel_id)]
    locations_availability = None  # TODO: find out cleaner way to augment plan with bin location finder
    
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('display_luggage.html', items=items, form=form, locations_availability=locations_availability)
        else:
            try:
                name = form.name.data.upper()
                ticket = form.ticket.data
                location = form.location.data
                bagCount = form.bagCount.data
                loggedInBy = form.loggedInBy.data.upper()
                comments = form.comments.data
                hotel_id = current_user.hotel_id
                entity = Luggage(name, ticket, location, bagCount, loggedInBy, comments, hotel_id)
                db.session.add(entity)
                db.session.commit()
                flash('Entry Submitted to Luggage Log.')
                return redirect(url_for('luggage.create_luggage'))
            except exc.SQLAlchemyError as e:
                flash('Entry NOT Submitted to Luggage Log.')
                return redirect(url_for('luggage.create_luggage'))

    return render_template('display_luggage.html', items=items, form=form, locations_availability=locations_availability)


@luggage.route('/ticket/<id>',  methods=['POST', 'GET'])
@login_required
def edit_ticket(id):
    if request.method == 'POST':
        id = request.form.get('id')

    luggage = Luggage.query.get(id)

    if request.method == 'POST':
        form = LuggageForm(request.form)
    else:
        form = LuggageForm(obj=luggage)

    locations_availability = None   # TODO: find out cleaner way to augment plan with bin location finder

    if request.method == 'POST':
        if not form.validate():
            # flash('All fields are required.')
            return render_template('edit_entry.html', form=form, locations_availability=locations_availability)
        else:
            try:
                form.populate_obj(luggage)

                luggage.lastModified = datetime.utcnow()
                luggage.modifiedBy = luggage.modifiedBy.upper()
                db.session.commit()
                flash('Entry saved')
                return redirect(url_for('luggage.create_luggage'))
            except exc.SQLAlchemyError as e:
                return 'Entry was not saved'



    return render_template('edit_entry.html', form=form, locations_availability=locations_availability)


@luggage.route('/ticket/<id>/complete', methods=['GET'])
@login_required
def complete_ticket(id):
    luggage = Luggage.query.get(id)
    loggedOutBy = re.sub(r'[\W]+', '', request.args.get('loggedOutBy'))

    # TODO: figure out why luggage returns None only on production, but works. Seems like the delete is happening twice
    # could be because of the call going to HTTP first, then HTTPS because of cloudflare
    try:
        if luggage:
            archive = Archive(luggage.name, luggage.ticket, luggage.location, luggage.bagCount, luggage.loggedInBy,
                              luggage.timeIn, luggage.modifiedBy, luggage.lastModified, luggage.hotel_id, loggedOutBy, luggage.comments)

            db.session.add(archive)
            db.session.delete(luggage)
            db.session.commit()
    except LockError:
        pass

    return redirect(url_for('luggage.create_luggage'))


def show_luggage():
    items = [item for item in Luggage.query.all()]
    return render_template("display_luggage.html", items=items)


@luggage.route('/search', methods=['POST'])
@login_required
def search():
    return redirect(url_for('luggage.search_results', query=g.search_form.search.data))


@luggage.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Luggage.query.whoosh_search("*" + query + "*", MAX_SEARCH_RESULTS).filter_by(hotel_id=current_user.hotel_id)
    return render_template('search_results.html', query=query, results=results)


@luggage.route('/archive', methods=['POST', 'GET'])
@login_required
def show_archive():
    return show_specific_archive(datetime.today().strftime("%Y%m%d"))

HOTEL_ROYAL_ID = 1

@luggage.route('/archive/<day>', methods=['POST', 'GET'])
@login_required
def show_specific_archive(day):
    archiveDate = datetime.strptime(day,"%Y%m%d")
    limitDate = archiveDate + timedelta(days=1)
    _archives = Archive.query.filter(Archive.timeIn >= archiveDate).filter(Archive.timeIn <= limitDate).order_by(Archive.timeIn.desc())
    if (current_user.hotel_id == HOTEL_ROYAL_ID):
        _archives = _archives.filter(or_(Archive.hotel_id==None, Archive.hotel_id==current_user.hotel_id))
    else:
        _archives = _archives.filter(Archive.hotel_id==current_user.hotel_id)
    
    daysBeforeToday = timedelta(days= (datetime.today() - archiveDate).days ).days
    daysBeforeToday = daysBeforeToday if (daysBeforeToday <= 5) else 5 
    printableDays = [archiveDate - timedelta(days=x) for x in range(-daysBeforeToday, 7)]
    return render_template("archive.html", entry=_archives, printableDays=printableDays, archiveDate=archiveDate)



@luggage.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form, (request.args.get('hotel'), False))
    if request.method == 'GET' or form.validate() == False:
        return render_template('login.html', form=form)
    username = form.username.data
    password = form.password.data
    registered_user = User.query.filter_by(username=username,password=password).first()
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('luggage.create_luggage'))



@luggage.route('/admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm(request.form, (request.args.get('hotel'), True))
    if request.method == 'GET' or form.validate() == False:
        return render_template('login_admin.html', form=form)
    username = form.username.data
    password = form.password.data
    registered_user = User.query.filter_by(username=username,password=password).first()
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('luggage.show_dashboard'))



@luggage.route("/admin/dashboard")
@login_required
# TODO: add admin permission check decorator
def show_dashboard():
    hotel_id = request.args.get('hotel')
    if hotel_id:
        if (hotel_id == str(HOTEL_ROYAL_ID)):
            current_archives = Archive.query.order_by(Archive.timeIn.desc()).filter(or_(Archive.hotel_id==None, Archive.hotel_id==hotel_id))
        else:
            current_archives = Archive.query.order_by(Archive.timeIn.desc()).filter_by(hotel_id=hotel_id)
    else:
        current_archives = Archive.query.order_by(Archive.timeIn.desc()).all()
    
    ### Get first and last store
    extra_info = get_first_and_last_stores(current_archives)
    storesByDay = extra_info['stores']
    ### Get luggage time (from storing to closing)
    luggage_times = get_luggage_time(current_archives)
    extra_info['luggage_time'] = luggage_times['luggage_time']
    ### Add luggage time to storesByDay
    for el in luggage_times['stores'].values():
        _key = el['day']
        storesByDay[_key]['diff'] = el['diff']
    
    ### Get amount of stores/logs per day
    stores_per_day = count_stores(current_archives)
    extra_info['count_store'] = stores_per_day['count_store']
    ### Add stores_per_day to storesByDay
    for el in stores_per_day['stores'].values():
        _key = el['day']
        storesByDay[_key]['count'] = el['count']
        storesByDay[_key]['hours'] = el['hours']
        storesByDay[_key]['hoursOut'] = el['hoursOut']
    
    ### Get amount of stores/logs per hour
    stores_per_hour = count_stores_by_hour(current_archives)
    extra_info['stores_by_hour'] = stores_per_hour['stores']
    
    hotels = Hotel.query.all()
    return render_template("dashboard.html", info=extra_info, hotels=hotels, hotel_id=hotel_id)



"""
@luggage.route("/password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form, current_user.password)
    
    if request.method == 'GET' or form.validate() == False:
        return render_template('change_password.html', form=form)
    
    current_user.password = form.password1.data
    db.session.commit()
    return redirect(url_for('luggage.create_luggage'))
"""

@luggage.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@luggage.route("/settings", methods=['GET', 'POST'])
@login_required
def change_hotel_settings():
    form = HotelForm(request.form, obj=current_user.hotel)
    
    if request.method == 'GET' or form.validate() == False:
        return render_template('hotel_settings.html', form=form, object=current_user.hotel)
    
    current_user.hotel.timezone = form.timezone.data
    db.session.commit()
    return redirect(url_for('luggage.create_luggage'))


@luggage.route("/")
def home():
    return render_template("home.html", hotels=Hotel.query.all())


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@luggage.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            current_user.hotel.image = filename
            db.session.commit()
            return redirect(url_for('luggage.change_hotel_settings', filename=filename))
    return render_template('hotel_upload_file.html')



@luggage.route('/media/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

