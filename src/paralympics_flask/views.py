from flask import current_app as app, render_template


# COMPLETED EXAMPLES OF WEEK 6 ACTIVITIES
# You can delete these once you've compared them to your work
@app.route('/html', methods=['GET'])
def index_html():
    """
    Returns a view using a basic HTML template with no CSS or Jinja.
    """
    return render_template('index_html.html')


@app.route('/css', methods=['GET'])
def index_css():
    """
    Returns a view using a basic HTML template with Bootstrap CSS.
    """
    return render_template('index_css.html')


@app.route('/responsive', methods=['GET'])
def index_responsive():
    """
    Returns a view using Bootstrap CSS and defines the viewport.
    """
    return render_template('index_responsive.html')


@app.route('/jinja', methods=['GET'])
def index_jinja():
    """
    Returns a view using a child Jinja template with Bootstrap CSS.
    """
    return render_template('index_jinja.html')


# STARTER CODE FOR ACTIVITY 7
@app.route('/', methods=['GET'])
def index():
    """
    Returns the home page.

     Use as the starting point for week 7 activities.
    """
    return render_template('index.html')