#importing libraries
import os
import numpy as np
import flask
import joblib  # Updated from sklearn.externals.joblib
import pandas as pd
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

#creating instance of the class
app = Flask(__name__, static_url_path='/static')

# Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "wine_cellar.sqlite")
model_path = os.path.join(basedir, "XGB_unscaled_model.pkl")

# Check if database exists, if not create it
if not os.path.exists(db_path):
    print(f"Warning: Database file not found at {db_path}")
    # Create an empty database with the required tables
    engine = create_engine(f'sqlite:///{db_path}')
    Base = automap_base()
    Base.metadata.create_all(engine)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1)

db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()

try:
    # reflect the tables
    Base.prepare(db.engine, reflect=True)
    
    # Save references to each table
    master_wine_table = Base.classes.master_wine_table
    wine_predictions = Base.classes.wine_predictions_table
except Exception as e:
    print(f"Error initializing database: {e}")
    master_wine_table = None
    wine_predictions = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story_of_wine')
def story_of_wine():
    return render_template('story_of_wine.html')

@app.route('/flavor_notes')
def flavor_notes():
    return render_template('flavor_notes.html')

@app.route('/virtual_sommelier')
def virtual_sommelier():
    return render_template('virtual_sommelier.html')

@app.route('/wine_recommender')
def wine_recommender():
    return render_template('wine_recommender.html')

@app.route('/predict_wine_score',methods=["POST"])   
def predict_wine_score():
    if request.method == 'POST':
        wine_type = request.form['wine_type']
        one_hot_wine_type = 0
        one_hot_wine_country = 0
        one_hot_taste = 0

        if wine_type == "White":
            one_hot_wine_type = 1
        else:
            one_hot_wine_type = 0

        taste_notes = request.form['taste_notes']
        wine_country = request.form['wine_country']
        wine_price = request.form['wine_price']

        if taste_notes == "light, fruity":
            one_hot_taste = 1
        else:
            one_hot_taste = 0

        if wine_country == "Austria":
            one_hot_wine_country = 1
        else:
            one_hot_wine_country = 0

        # Clean the data by convert from unicode to float 
        sample_data = [one_hot_wine_type, one_hot_taste, wine_price, one_hot_wine_country]
        clean_data = [float(i) for i in sample_data]

        # Reshape the Data as a Sample not Individual Features
        feed_AI = np.array(clean_data).reshape(1,-1)

        try:
            if os.path.exists(model_path):
                XGB_model = joblib.load(model_path)
                predicted_score = XGB_model.predict(feed_AI)
            else:
                print(f"Warning: Model file not found at {model_path}")
                predicted_score = [0]
        except Exception as e:
            print(f"Error loading model: {e}")
            predicted_score = [0]

        message = ""

        if predicted_score < 85:
            message = "Not bad..."
        elif predicted_score >= 85 and predicted_score < 90:
            message = "DDDDelicious!!"
        elif predicted_score >= 90:
            message = "Mmmmm Mmmmm Mmmmmmm...  Now that's the good stuff!!!!"

    test_1 = "test_1_value..."

    return render_template('virtual_sommelier.html', testing_1=test_1, wine_type=wine_type, one_hot_wine_type=one_hot_wine_type, taste_notes=taste_notes, wine_country=wine_country, 
                           wine_price=wine_price, feed_AI=feed_AI, predicted_score=round(predicted_score[0], 2), message=message)

@app.route('/recommend_wines', methods=["POST"])
def recommend_wines():
    if master_wine_table is None:
        return jsonify({"error": "Database not available"})
        
    taste_notes = request.form['taste_notes']
    wine_type = request.form['wine_type']
    wine_country = request.form['wine_country']
    # Use Pandas to perform the sql query
    stmt = db.session.query(master_wine_table).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    wine_list = df.to_list()
    wine_list_jsonified = jsonify(wine_list)

    return (wine_list_jsonified)

if __name__ == "__main__":
    app.run(debug=True)