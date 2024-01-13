# COMP0034 Week 7 Coding activities: 

## Set-up

1. Fork the repository
2. Clone the forked repository to create a project in your IDE
3. Create and activate a virtual environment in the project folder e.g.

    - MacOS: `python3 -m venv .venv` then `source .venv/bin/activate`
    - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
4. Check `pip` is the latest versions: `pip install --upgrade pip`
5. Install the requirements. You may wish to edit [requirements.txt](requirements.txt) first to remove the packages for
   Flask or Dash if you only want to complete the activities for one type of app.

    - e.g. `pip install -r requirements.txt`
6. Install the paralympics app code e.g. `pip install -e .`

## Activity instructions

The activities ...

There are two versions of the activities. You can complete both, or just the version for the framework you intend
to use for coursework 2. Dash is for dashboard apps (apps that mostly contain charts); Flask is for any other app e.g.
pages that include a feature that uses a machine learning model or pages that work with the data in some other way.

1. [Dash activities](activities/1-dash.md)
2. [Flask activities](activities/1-flask.md)
