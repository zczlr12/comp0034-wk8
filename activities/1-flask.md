# Flask version of the activities

## Check the Flask app runs

Check that the app runs before starting any of the activities.

1. `flask --app paralympics_flask run --debug`

   You may need to change the port number if you already have something running on the default port 5000
   e.g. `flask --app paralympics_flask run --debug --port=5050`.
2. Go to the URL that is shown in the terminal. By default, this is http://127.0.0.1:5000
3. Stop the app using `CTRL+C`

## Flask page activities

Some of the page activities are in week 7. This week covers those that involve a form. 

| Week | Page                                                                                                                  | Data access                                       | Route                                                                                                                                                        | Jinja                                                                                        | Form                                                              | Other                                                        |
|:-----|:----------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------|:------------------------------------------------------------------|:-------------------------------------------------------------|
| 7    | [Event details](https://github.com/nicholsons/comp0034-wk7/blob/master/activities/flask-1-event-page.md)              | SQLAlchemy query                                  | GET: Find an event by id and pass it to the template                                                                                                         | Template with bootstrap rows and columns                                                     |                                                                   |                                                              |
| 7    | [Home with hyperlinked logos](https://github.com/nicholsons/comp0034-wk7/blob/master/activities/flask-2-home-page.md) | SQLAlchemy query                                  | GET: Find all events and pass to the template                                                                                                                | Template with for loop generates logos + event year & host + hyperlink to events detail page |                                                                   | Access image files from /static<br>Dynamically generate URL. |
| 7    | [Chart](https://github.com/nicholsons/comp0034-wk7/blob/master/activities/flask-3-chart-page.md)                      | SQLAlchemy query with results to pandas DataFrame | GET: Get the HTML for the chart and pass to the template                                                                                                     | Displays HTML. Prevents auto-escaping of the variable with the HTML.                         |                                                                   |                                                              |
| 8    | [Add event](../activities/flask-1-add-event-page.md)                                                                  |                                                   | GET: Display the add event form.<br>POST: Use the values from the form to create a SQLAlchemy object and save to the database.                               |                                                                                              | Form to add fields for a new event. Validation. Form field macro. |                                                              |
| 8    | [Prediction](../activities/flask-2-prediction.md)                                                                     | Use model.pkl to get a prediction                 | GET: Display the prediction form.<br>POST: Pass the values from the form to the model to get a prediction, update the page to display the prediction result. | Template with form and placeholder `<div>` for the prediction result.                        | Form to enter values for prediction. Validation. Default values.  | Create pickled ML model.                                     |
