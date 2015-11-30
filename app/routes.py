import os
from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, session, g, redirect, url_for, render_template, request, flash
from forms import LuggageForm
from models import Luggage, db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from sqlalchemy import exc

luggage = Blueprint('luggage', __name__, template_folder='templates')
  
@luggage.route('/create', methods=['GET', 'POST'])
def create_luggage():
    form = LuggageForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('create_luggage.html', form=form)
        else:
            try:
                name = form.name.data
                ticket = form.ticket.data
                location = form.location.data
                bagCount = form.bagCount.data
                entity = Luggage(name, ticket, location, bagCount, None)
                db.session.add(entity)
                db.session.commit()
                return 'Entry Submitted to Luggage Log.'
            except exc.SQLAlchemyError as e:
                return 'Entry NOT Submitted to Luggage Log.'

    return render_template('create_luggage.html', form=form)

@luggage.route('/')
def show_luggage():
    items = [item for item in Luggage.query.all()]
    return render_template("display_luggage.html", items=items)
  
