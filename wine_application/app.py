#importing libraries
import os
import numpy as np
import flask
import joblib  # Updated from sklearn.externals.joblib
from flask_material import Material
import pandas as pd
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Get the absolute path to the directory containing this file
base_dir = os.path.abspath(os.path.dirname(__file__))

# Verify critical directories exist
template_dir = os.path.join(base_dir, 'parallax-template', 'templates')
static_dir = os.path.join(base_dir, 'parallax-template', 'static')

if not os.path.exists(template_dir):
    raise RuntimeError(f"Template directory not found at: {template_dir}")
if not os.path.exists(static_dir):
    raise RuntimeError(f"Static directory not found at: {static_dir}")

#creating instance of the class
app = Flask(__name__, 
    static_url_path='/static',
    static_folder=static_dir,
    template_folder=template_dir)
Material(app)

# Database Setup - PostgreSQL only
if 'DATABASE_URL' not in os.environ:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in your environment or deployment platform.")

database_url = os.environ['DATABASE_URL']
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print(f"Initializing PostgreSQL database connection... (URL prefix: {database_url[:15]}...)")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20  # Adjust pool size for better performance
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 5  # Allow some overflow connections

db = SQLAlchemy(app)

# Define the tables
class MasterWineTable(db.Model):
    __tablename__ = 'master_wine_table'
    id = db.Column(db.Integer, primary_key=True)
    wine_type = db.Column(db.String(50))
    taste_notes = db.Column(db.String(100))
    wine_country = db.Column(db.String(50))
    wine_price = db.Column(db.Float)
    wine_score = db.Column(db.Float)

class WinePredictionsTable(db.Model):
    __tablename__ = 'wine_predictions_table'
    id = db.Column(db.Integer, primary_key=True)
    predicted_score = db.Column(db.Float)
    actual_score = db.Column(db.Float)

try:
    # Create tables if they don't exist
    db.create_all()
    print("✓ Database tables verified/created successfully")
    
    # Verify tables exist
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    print(f"✓ Available tables: {table_names}")
    
    # Test database connection
    with db.engine.connect() as conn:
        conn.execute(sqlalchemy.text("SELECT 1"))
        print("✓ Database connection test successful")
    
    # Set up references for queries
    master_wine_table = MasterWineTable
    wine_predictions = WinePredictionsTable
    
except Exception as e:
    print(f"❌ Error initializing PostgreSQL database: {str(e)}")
    print(f"Database URL being used (redacted): {database_url[:15]}...{database_url[-15:]}")
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

@app.route('/predict_wine_score', methods=["POST"])
def predict_wine_score():
    if master_wine_table is None:
        return jsonify({"error": "Database not available"})

    wine_type = request.form['wine_type']
    taste_notes = request.form['taste_notes']
    wine_country = request.form['wine_country']
    wine_price = float(request.form['wine_price'])
    
    try:
        # Here you would normally do the prediction
        # For now, returning a mock prediction
        predicted_score = 88.5  # Replace with actual prediction logic
        message = "This is a good wine choice!"
        
        return render_template('virtual_sommelier.html',
                             wine_type=wine_type,
                             taste_notes=taste_notes,
                             wine_country=wine_country,
                             wine_price=wine_price,
                             predicted_score=predicted_score,
                             message=message)
    except Exception as e:
        print(f"Error predicting score: {str(e)}")
        return render_template('virtual_sommelier.html', error="Failed to predict wine score")

@app.route('/recommend_wines', methods=["POST"])
def recommend_wines():
    if master_wine_table is None:
        return jsonify({"error": "Database not available"})

    taste_notes = request.form['taste_notes']
    wine_type = request.form['wine_type']
    wine_country = request.form['wine_country']
    
    try:
        # Use Pandas to perform the sql query
        stmt = db.session.query(master_wine_table).statement
        df = pd.read_sql_query(stmt, db.session.bind)
        wine_list = df.to_dict(orient='records')
        return jsonify(wine_list)
    except Exception as e:
        print(f"Error querying database: {str(e)}")
        return jsonify({"error": f"Database query failed: {str(e)}"})

@app.route('/get_wine_rating', methods=["POST"])
def get_wine_rating():
    if wine_predictions is None:
        return jsonify({"error": "Database not available"})
        
    try:
        stmt = db.session.query(wine_predictions).statement
        df = pd.read_sql_query(stmt, db.session.bind)
        predictions = df.to_dict(orient='records')
        return jsonify(predictions)
    except Exception as e:
        print(f"Error querying predictions: {str(e)}")
        return jsonify({"error": f"Database query failed: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)