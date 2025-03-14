import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import psycopg2
from urllib.parse import urlparse

def migrate_to_postgres():
    # SQLite connection
    sqlite_path = "wine_cellar.sqlite"
    sqlite_conn = sqlite3.connect(sqlite_path)
    
    # Read tables from SQLite
    master_wine_df = pd.read_sql_query("SELECT * FROM master_wine_table", sqlite_conn)
    wine_predictions_df = pd.read_sql_query("SELECT * FROM wine_predictions_table", sqlite_conn)
    
    # Get PostgreSQL URL from environment variable
    postgres_url = os.environ.get('DATABASE_URL')
    if not postgres_url:
        print("Error: DATABASE_URL environment variable not set")
        return
    
    # Parse the URL and create PostgreSQL connection
    parsed = urlparse(postgres_url)
    dbname = parsed.path[1:]
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    
    # Create PostgreSQL engine
    postgres_engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    
    # Create tables in PostgreSQL
    master_wine_df.to_sql('master_wine_table', postgres_engine, if_exists='replace', index=False)
    wine_predictions_df.to_sql('wine_predictions_table', postgres_engine, if_exists='replace', index=False)
    
    print("Migration completed successfully!")
    
    # Close connections
    sqlite_conn.close()
    postgres_engine.dispose()

if __name__ == "__main__":
    migrate_to_postgres() 