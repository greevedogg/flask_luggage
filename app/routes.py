# import os
# from sqlite3 import dbapi2 as sqlite3
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import Form
# from wtforms import validators
# import flask.ext.whooshalchemy
from flask import Blueprint, session, g, redirect, url_for, render_template, request, flash
from forms import LuggageForm, SearchForm
from models import Luggage, db, Archive, Location
from sqlalchemy import exc
from config import MAX_SEARCH_RESULTS
import re
from datetime import datetime
import json


luggage = Blueprint('luggage', __name__, template_folder='templates')


@luggage.before_request
def before_request():
    g.search_form = SearchForm(request.form)


@luggage.route('/', methods=['GET', 'POST'])
def create_luggage():
    form = LuggageForm(request.form)

    items = [item for item in Luggage.query.order_by(Luggage.timeIn.desc()).all()]
    locations_availability = Location().availability()

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
                entity = Luggage(name, ticket, location, bagCount, loggedInBy, None)
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

    if request.method == 'POST':
        if not form.validate():
            # flash('All fields are required.')
            return render_template('edit_entry.html', form=form)
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

    locations_availability = Location().availability()

    return render_template('edit_entry.html', form=form, locations_availability=locations_availability)


@luggage.route('/ticket/<id>/complete', methods=['GET'])
def complete_ticket(id):
    luggage = Luggage.query.get(id)
    loggedOutBy = re.sub(r'[\W]+', '', request.args.get('loggedOutBy'))

    archive = Archive(luggage.name, luggage.ticket, luggage.location, luggage.bagCount, luggage.loggedInBy,
                      luggage.timeIn, luggage.modifiedBy, luggage.lastModified, loggedOutBy, luggage.comments)

    db.session.add(archive)
    db.session.delete(luggage)
    db.session.commit()

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
    entry = [item for item in Archive.query.order_by(Archive.timeIn.desc()).all()]
    return render_template("archive.html", entry=entry)
