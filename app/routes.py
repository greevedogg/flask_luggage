# import os
# from sqlite3 import dbapi2 as sqlite3
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import Form
# from wtforms import validators
# import flask.ext.whooshalchemy
from flask import Blueprint, session, g, redirect, render_template, request, flash
from helpers import url_for
from forms import LuggageForm, SearchForm
from models import Luggage, db, Archive, Location
from sqlalchemy import exc
from config import MAX_SEARCH_RESULTS
import re
from datetime import datetime, timedelta
import json
from whoosh.index import LockError


luggage = Blueprint('luggage', __name__, template_folder='templates')


@luggage.before_request
def before_request():
    g.search_form = SearchForm(request.form)


@luggage.route('/', methods=['GET', 'POST'])
def create_luggage():
    form = LuggageForm(request.form)

    items = [item for item in Luggage.query.order_by(Luggage.timeIn.desc()).all()]
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
                entity = Luggage(name, ticket, location, bagCount, loggedInBy, comments)
                db.session.add(entity)
                db.session.commit()
                flash('Entry Submitted to Luggage Log.')
                return redirect(url_for('luggage.create_luggage'))
            except exc.SQLAlchemyError as e:
                flash('Entry NOT Submitted to Luggage Log.')
                return redirect(url_for('luggage.create_luggage'))

    return render_template('display_luggage.html', items=items, form=form, locations_availability=locations_availability)


@luggage.route('/ticket/<id>',  methods=['POST', 'GET'])
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
def complete_ticket(id):
    luggage = Luggage.query.get(id)
    loggedOutBy = re.sub(r'[\W]+', '', request.args.get('loggedOutBy'))

    # TODO: figure out why luggage returns None only on production, but works. Seems like the delete is happening twice
    # could be because of the call going to HTTP first, then HTTPS because of cloudflare
    try:
        if luggage:
            archive = Archive(luggage.name, luggage.ticket, luggage.location, luggage.bagCount, luggage.loggedInBy,
                              luggage.timeIn, luggage.modifiedBy, luggage.lastModified, loggedOutBy, luggage.comments)

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
def search():
    return redirect(url_for('luggage.search_results', query=g.search_form.search.data))


@luggage.route('/search_results/<query>')
def search_results(query):
    results = Luggage.query.whoosh_search("*" + query + "*", MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)


@luggage.route('/archive', methods=['POST', 'GET'])
def show_archive():
    return show_specific_archive(datetime.today().strftime("%Y%m%d"))


@luggage.route('/archive/<day>', methods=['POST', 'GET'])
def show_specific_archive(day):
    archiveDate = datetime.strptime(day,"%Y%m%d")
    limitDate = archiveDate + timedelta(days=1)
    _archives=Archive.query.filter(Archive.timeIn >= archiveDate).filter(Archive.timeIn <= limitDate).order_by(Archive.timeIn.desc()).all()
    entry = [item for item in _archives]
    
    daysBeforeToday = timedelta(days= (datetime.today() - archiveDate).days ).days
    daysBeforeToday = daysBeforeToday if (daysBeforeToday <= 5) else 5 
    printableDays = [archiveDate - timedelta(days=x) for x in range(-daysBeforeToday, 7)]
    return render_template("archive.html", entry=entry, printableDays=printableDays, archiveDate=archiveDate)
