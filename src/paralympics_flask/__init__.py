import os
from pathlib import Path

import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='create-your-own-key',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'paralympics.sqlite'),
    )
    if test_config:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from paralympics_flask.models import User, Event, Region
    with app.app_context():
        db.create_all()
        add_data_from_csv()

        from paralympics_flask import views

    return app


def add_data_from_csv():
    """Adds data to the database if it does not already exist."""

    from paralympics_flask.models import Region, Event

    # If there are no regions in the database, then add them
    first_region = db.session.execute(db.select(Region)).first()
    if not first_region:
        print("Start adding region data to the database")
        noc_file = Path(__file__).parent.parent.parent.joinpath("data", "noc_regions.csv")
        with open(noc_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                r = Region(NOC=row[0], region=row[1], notes=row[2])
                db.session.add(r)
            db.session.commit()

    # If there are no Events, then add them
    first_event = db.session.execute(db.select(Event)).first()
    if not first_event:
        print("Start adding event data to the database")
        event_file = Path(__file__).parent.parent.parent.joinpath("data", "paralympic_events.csv")
        with open(event_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                e = Event(type=row[0],
                          year=row[1],
                          country=row[2],
                          host=row[3],
                          NOC=row[4],
                          start=row[5],
                          end=row[6],
                          duration=row[7],
                          disabilities_included=row[8],
                          countries=row[9],
                          events=row[10],
                          sports=row[11],
                          participants_m=row[12],
                          participants_f=row[13],
                          participants=row[14],
                          highlights=row[15])
                db.session.add(e)
            db.session.commit()
