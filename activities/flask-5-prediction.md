# Page that returns a prediction

There is no ML model for the paralympics app so this example creates a simple one-page Flask app with a form to predict
the species of Iris.

The code in the src/flask_iris directory structure creates a basic Flask app that includes a form to get a prediction
from a pickled model.

## Form
There is a form defined in [/src/flask_iris/forms.py](../src/flask_iris/forms.py) which 4 fields for each value required
to get a prediction.

How to create a form is covered in activity 4.

## Route
There is a single route in [src/flask_iris/routes.py](../src/flask_iris/routes.py) which on GET returns a form, and on
POST if all the fields of the form have been completed, returns a prediction which is appended to the page below the
form.

The route looks like this:

```python
@app.route("/", methods=["GET", "POST"])
def index():
    # Create an instance of a PredictionForm which uses the class in forms.py
    form = PredictionForm()

    # If the form has been submitted and passes validation rules set in forms.py
    if form.validate_on_submit():
        # Get all values from the form
        features_from_form = [
            form.sepal_length.data,
            form.sepal_width.data,
            form.petal_length.data,
            form.petal_width.data,
        ]

        # Make the prediction (see function in the routes.py file)
        prediction = make_prediction(features_from_form)

        prediction_text = f"Predicted Iris type: {prediction}"

        # return to the homepage and append text to the page that shows the prediction result
        return render_template(
            "index.html", form=form, prediction_text=prediction_text
        )
    # Return the homepage with the default form
    return render_template("index.html", form=form)
```

The function to make a prediction is as follows:

```python
import numpy as np
import pickle
from pathlib import Path


def make_prediction(flower_values):
    """Takes the flower values, makes a model using the prediction and returns a string of the predicted flower variety

    Parameters:
    flower_values (List): List of sepal length, sepal width, petal length, petal width

    Returns:
    variety (str): Name of the predicted iris variety
    """

    # Convert to a 2D numpy array with float values, needed as input to the model
    input_values = np.asarray([flower_values], dtype=float)

    # Get a prediction from the model
    pickle_file = Path(__file__).parent.joinpath("model.pkl")
    model = pickle.load(open(pickle_file, "rb"))
    prediction = model.predict(input_values)

    # convert the prediction to the variety name
    varieties = {0: "iris-setosa", 1: "iris-versicolor", 2: "iris-virginica"}
    variety = np.vectorize(varieties.__getitem__)(prediction[0])

    return variety
```

## Pickled model
The code to generate and pickle the model is in [/src/flask_iris/create_ml_model.py](../src/flask_iris/create_ml_model.py).

This code is called in the create_app() function in the `flask_iris/__init__.py` file

```python
from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle


def create_model(alg):
    """Creates a model using the algorithm provided. Output serialised using pickle.
    
    Args:
    alg: either lr (LogisticRegression) or dt (DecisionTreeClassifier)

    Returns:
    .pkl Pickled model

    """
    # Check if the model.pkl file exists, create it if it doesn't
    path_exists = Path.exists(Path(__file__).parent.joinpath("model.pkl"))
    if not path_exists:
        iris_file = Path(__file__).parent.joinpath("data", "iris.csv")
        df = pd.read_csv(iris_file)

        # Convert categorical data to numeric
        le = LabelEncoder()
        df["species"] = le.fit_transform(df["species"])

        # X = feature values (case sepal length, sepal width, petal length, petal width)
        X = df.iloc[:, 0:-1]
        X = X.values
        # y = target values, last column of the data frame
        y = df.iloc[:, -1]

        # Split the data into 80% training and 20% testing (type of iris)
        x_train, x_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Initialize the model
        if alg == "dt":
            model = DecisionTreeClassifier()
        elif alg == "lr":
            model = LogisticRegression()
        else:
            raise ValueError("Must provide either 'dt' (DecisionTree) or 'lr' (LogisticRegression)")

        # Train the model
        model.fit(x_train, y_train)

        # Pickle the model and save current folder
        pickle_file = Path(__file__).parent.joinpath("model.pkl")
        pickle.dump(model, open(pickle_file, "wb"))
```
## Run the app

To run the app: `flask --app flask_iris:create(app) run --debug`
