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

#creating instance of the class
app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static',
    template_folder='templates')
Material(app)

# Database Setup
database_url = os.environ.get('DATABASE_URL', 'sqlite:///wine_cellar.sqlite')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()

try:
    # reflect the tables
    Base.prepare(db.engine, reflect=True)
    
    # Save references to each table
    master_wine_table = Base.classes.master_wine_table
    wine_predictions = Base.classes.wine_predictions_table
    
    # Verify tables exist
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    print(f"Available tables: {table_names}")
    
except Exception as e:
    print(f"Error initializing database: {str(e)}")
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