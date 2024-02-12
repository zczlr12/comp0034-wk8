# Add event page

For this page I suggest:

- Create a form that matches the values needed
- Create a template that displays the form and provides a button to submit the changes
- Create a route that on GET displays the form with the data, and on POST (form submission) checks the fields are valid
  and if they are saves the updates to the database.

## Form

To create a form, install [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/). This is a Flask wrapper for
the [WTForms](https://wtforms.readthedocs.io/en/3.1.x/) package.

You also need to install [WTForms-SQLAlchemy](https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/)
for the QuerySelectField.

You will use a Flask-WTF form class to define the form that will be displayed on the web page that allows someone to add
a new event.

The form should have a field that matches each of the fields needed for the Event class (except the id as this is added
by the database).

The form fields should match the data types of the SQLAchemy Event class. You can also add validation rules.

To define a form start with
the [Flask-WTF documentation](https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/#creating-forms).

WTForms provides guidance on secure forms, file uploads and recaptcha. For other fields types you will need to
refer to the [WTForms documentation](https://wtforms.readthedocs.io/en/3.0.x/).

Add the following form to the forms.py module. This includes examples of different types of form fields:

```python
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField, StringField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from paralympics_flask import db
from paralympics_flask.models import Region


def get_countries():
    return db.session.execute(db.select(Region).order_by(Region.region)).scalars()


class EventForm(FlaskForm):
    # the names of the fields exactly match the attributes of the Event class for convenience
    # Drop down selection with options specified in the form class.
    type = SelectField('Event type', choices=[('summer', 'Summer'), ('winter', 'Winter')], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), ], render_kw={"placeholder": 2020})
    # Select the country from a dropdown list based on the Region table.
    # Uses WTForms-SQLAlchemy https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/
    country = QuerySelectField('Country', query_factory=get_countries, get_label='region')
    # 'NOC' is a foreign key determined by country, this will be determined in the route code
    # Alternate validation syntax, see https://wtforms.readthedocs.io/en/3.1.x/fields/#field-definitions
    host = StringField('Host city', [validators.optional()])
    start = DateField('Start date', [validators.data_required()])
    end = DateField('End date', [validators.data_required()])
    # 'duration' is omitted as this will be calculated in the route code when saved to the database
    disabilities_included = SelectMultipleField('Disabilities included',
                                                choices=[('Spinal injury', 'Spinal injury'), ('Amputee', 'Amputee'),
                                                         ('Vision Impairment', 'Vision Impairment'),
                                                         ('Cerebral Palsy', 'Cerebral Palsy'),
                                                         ('Les Autres', 'Les Autres'),
                                                         ('Intellectual Disability', 'Intellectual Disability')])
    countries = IntegerField('Total number of participating countries', [validators.optional()])
    events = IntegerField('Total number of events', [validators.optional()])
    sports = IntegerField('Total number of sports', [validators.optional()])
    participants_m = IntegerField('Total number of male participants', [validators.optional()])
    participants_f = IntegerField('Total number of female participants', [validators.optional()])
    participants = IntegerField('Total number of participants', [validators.optional()])
    highlights = TextAreaField('Highlights', [validators.optional(), validators.length(max=200)])

    # 'NOC' is a foreign key determined by country, this will be added in the route code
    # 'duration' will be calculated in the route code
```

## Template

The template needs to generate an HTML form that matches the fields in the database.

You can define each field; though if you have a lot of fields you can use a Jinja macro that generates them for you.

The macro code has been saved in the /templates directory as form_macros.html. There is one macro to render a field and
another that will render all the fields in the form.

Create an add_event.html template. The first below imports the render_field macro.

```html
{% from "form_macros.html" import render_field, render_form %}

{% extends 'base.html' %}

{% block title %}Add new event{% endblock %}

{% block content %}
<h4>Enter the details for the paralympics</h4>
<form method="post" novalidate>
    <div class="col-md-6">
        <!-- Uses macro to render the fields in the form -->
        {{ render_field(form.country) }}
        {{ render_field(form.year) }}
        {{ render_field(form.type) }}
        {{ render_field(form.host) }}
        {{ render_field(form.start) }}
        {{ render_field(form.end) }}
        {{ render_field(form.sports) }}
        {{ render_field(form.countries) }}
        {{ render_field(form.events) }}
        {{ render_field(form.participants) }}
        {{ render_field(form.participants_m) }}
        {{ render_field(form.participants_f) }}
        {{ render_field(form.disabilities_included) }}
        {{ render_field(form.highlights) }}
        <button type="submit" class="btn btn-primary">Submit</button>
    </div>
</form>
{% endblock %}
```

## Route

The route needs to receive two types of request:

- GET: When the page is first loaded, this returns and empty form
- POST: When the form is submitted

The GET route logic is:

1. Create an instance of an EventForm
2. Render the template for the add_event page and pass the form to it

The POST route logic is:

1. Check the form passes the validation that was set in the EventForm class
    - if not, render the template for the add_event page and pass the form to it
2. If yes, create the event object:
    - Create an empty event object
    - Add attributes to the event object using the form fields
    - Change the event.country from an object to just the region name
    - Find the region to add the foreign key field to the event
    - Calculate the duration by subtracting the start date from the end date if they are not None. The result will be a
      timedelta so get an int, access just the days element of the timedelta
    - `disabilites_included` value from the form is a list even when it is empty. The database expects a string not a
      list so this needs to be converted.
3. Check that the event host and year do not already exist in the database
   - if they do then return an error message render the template for the add_event page and pass the form to it.
4. If not existing, try to save the event to the database.
   - If fails, flash an error message and render the template for the add_event page and pass the form to it.
5. If the event is saved, flash a success message and redirect to the route for the home page.

The above introduces two new Flask functions:

   - [Redirect](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.redirect) to a different route
   - [message flashing](https://flask.palletsprojects.com/en/3.0.x/patterns/flashing/)


```python
from flask import current_app as app, render_template, flash, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from paralympics_flask import db
from paralympics_flask.forms import EventForm
from paralympics_flask.models import Event, Region


@app.route("/events", methods=["GET", "POST"])
def add_event():
    """ Adds a new event to the database. """
    # Form, with the current form values if there are any
    form = EventForm(request.form)

    if form.validate_on_submit():
        # Empty event object
        event = Event()

        # Add attributes to the event object using the form fields
        form.populate_obj(event)

        # Change the event.country from an object to just the region name
        country = event.country.region
        event.country = country

        # Find the region to add the foreign key field to the event
        region = db.session.execute(db.select(Region).filter_by(region=country)).scalar_one()
        event.NOC = region.NOC

        # Calculate the duration by subtracting the start date from the end date if they are not None
        if event.start and event.end:
            duration = event.end - event.start
            # duration is a timedelta so get just the days as this will be an int
            event.duration = duration.days

        # disabilites_included from the form is a list even when empty, the database expects a string not a list
        # Convert the list to a string
        disabilities = ','.join(map(str, event.disabilities_included))
        event.disabilities_included = disabilities

        # Check that the event host and year do not already exist.
        exists = db.session.execute(db.select(Event).filter_by(country=event.country, year=event.year)).first()
        if not exists:
            try:
                db.session.add(event)
                db.session.commit()
                # If successful, return to the homepage and use Flask Flash to display a success message
                flash('Event added!', 'success')
                return redirect(url_for('index'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'An error occured while saving.{e}', 'error')
                return render_template('add_event.html', form=form)
        else:
            flash('This event already exists.', 'error')
            render_template('add_event.html', form=form)
    # Otherwise display the page with the Event template
    return render_template('add_event.html', form=form)
```

## Run the app


TODO: Update the navbar
