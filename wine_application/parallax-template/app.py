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

# ML Pkg
from sklearn.externals import joblib

# Get the absolute path to the directory containing this file
base_dir = os.path.abspath(os.path.dirname(__file__))

#creating instance of the class
app = Flask(__name__, 
    static_url_path='/static',
    static_folder=os.path.join(base_dir, 'static'),
    template_folder=os.path.join(base_dir, 'templates'))
Material(app)

# Database Setup - PostgreSQL only
if 'DATABASE_URL' not in os.environ:
    raise ValueError("DATABASE_URL environment variable is not set")

database_url = os.environ['DATABASE_URL']
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print(f"Using PostgreSQL database: {database_url}")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    print("Tables verified/created successfully")
    
    # Verify tables exist
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    print(f"Available tables: {table_names}")
    
    # Test database connection
    with db.engine.connect() as conn:
        conn.execute(sqlalchemy.text("SELECT 1"))
        print("Database connection test successful")
    
    # Set up references for queries
    master_wine_table = MasterWineTable
    wine_predictions = WinePredictionsTable
    
except Exception as e:
    print(f"Error initializing database: {str(e)}")
    print(f"Database URL being used: {database_url}")
    master_wine_table = None
    wine_predictions = None

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
        wine_list = df.to_dict(orient='records')  # Changed from to_list() to to_dict()
        return jsonify(wine_list)
    except Exception as e:
        print(f"Error querying database: {str(e)}")
        return jsonify({"error": f"Database query failed: {str(e)}"})

# ... rest of your existing code ...