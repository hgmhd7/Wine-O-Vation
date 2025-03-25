import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
import sqlite3
import psycopg2
from urllib.parse import urlparse
import argparse
import time

def test_postgres_connection(url):
    """Test the PostgreSQL connection and print detailed information."""
    print("\nTesting PostgreSQL connection...")
    try:
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        
        # Parse the URL for logging (hide password)
        parsed = urlparse(url)
        safe_url = f"postgresql://{parsed.username}:***@{parsed.hostname}:{parsed.port}{parsed.path}"
        print(f"Attempting to connect to: {safe_url}")
        
        # Try to connect
        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Successfully connected to PostgreSQL!")
            return True
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        return False

def get_row_count(engine, table_name):
    """Get the number of rows in a table."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            return result.scalar()
    except Exception:
        return 0

def verify_migration(sqlite_engine, postgres_engine, tables):
    """Verify that all data was migrated correctly."""
    print("\nVerifying migration...")
    all_valid = True
    
    for table_name in tables:
        sqlite_count = get_row_count(sqlite_engine, table_name)
        postgres_count = get_row_count(postgres_engine, table_name)
        
        print(f"\nTable: {table_name}")
        print(f"SQLite rows: {sqlite_count}")
        print(f"PostgreSQL rows: {postgres_count}")
        
        if sqlite_count != postgres_count:
            print(f"WARNING: Row count mismatch for table {table_name}!")
            all_valid = False
    
    return all_valid

def migrate_to_postgres(postgres_url):
    print("Starting migration process...")
    
    # Create database connections
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sqlite_path = os.path.join(script_dir, "parallax-template", "wine_cellar.sqlite")
    
    # Print SQLite file size
    if os.path.exists(sqlite_path):
        size_mb = os.path.getsize(sqlite_path) / (1024 * 1024)
        print(f"\nSQLite database size: {size_mb:.2f} MB")
    else:
        print(f"\nERROR: SQLite file not found at {sqlite_path}")
        return
        
    sqlite_engine = create_engine(f'sqlite:///{sqlite_path}')
    postgres_engine = create_engine(postgres_url)
    
    try:
        # Test PostgreSQL connection
        with postgres_engine.connect() as conn:
            print("Successfully connected to PostgreSQL database")
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return

    print(f"Found SQLite database at {sqlite_path}, migrating data...")
    
    # Get list of tables from SQLite
    inspector = inspect(sqlite_engine)
    tables = inspector.get_table_names()
    print(f"\nFound {len(tables)} tables in SQLite: {', '.join(tables)}")
    
    for table_name in tables:
        print(f"\nMigrating table: {table_name}")
        
        # Get total rows in SQLite for this table
        total_sqlite_rows = get_row_count(sqlite_engine, table_name)
        print(f"Total rows in SQLite: {total_sqlite_rows}")
        
        # Check existing rows in PostgreSQL
        existing_rows = get_row_count(postgres_engine, table_name)
        print(f"Found {existing_rows} existing rows in PostgreSQL table")
        
        if existing_rows >= total_sqlite_rows:
            print(f"Table {table_name} appears to be fully migrated, skipping...")
            continue
        
        # Read data from SQLite in chunks
        chunk_size = 100  # Reduced chunk size
        offset = existing_rows  # Start from where we left off
        total_rows = existing_rows
        
        while True:
            try:
                # Read chunk from SQLite
                query = f"SELECT * FROM {table_name} LIMIT {chunk_size} OFFSET {offset}"
                chunk = pd.read_sql_query(query, sqlite_engine)
                
                if chunk.empty:
                    break
                    
                total_rows += len(chunk)
                print(f"Read {len(chunk)} rows from SQLite (Total: {total_rows}/{total_sqlite_rows})")
                
                # Always append since we're starting from the correct offset
                if_exists = 'append' if existing_rows > 0 else 'replace'
                
                # Try to write to PostgreSQL with retries
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        chunk.to_sql(table_name, postgres_engine, if_exists=if_exists, index=False)
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            print(f"Failed to migrate chunk after {max_retries} attempts. Error: {e}")
                            raise
                        print(f"Retry {retry_count}/{max_retries} after error: {e}")
                        time.sleep(2)  # Wait 2 seconds before retrying
                
                print(f"Migrated rows {offset + 1} to {offset + len(chunk)}")
                offset += chunk_size
                
                # Add a small delay between chunks to prevent overwhelming the server
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error during migration at offset {offset}: {e}")
                print("You can restart the migration with the same command - it will continue from where it left off")
                return
    
    # Verify the migration
    if verify_migration(sqlite_engine, postgres_engine, tables):
        print("\nMigration completed successfully and verified!")
    else:
        print("\nMigration completed but verification failed - some tables may need to be re-migrated")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Migrate SQLite database to PostgreSQL')
    parser.add_argument('--url', required=True, help='PostgreSQL database URL')
    args = parser.parse_args()
    migrate_to_postgres(args.url)