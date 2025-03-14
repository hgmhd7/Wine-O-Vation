import os
import shutil

def setup_files():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source files
    source_db = os.path.join(current_dir, 'wine_application', 'wine_cellar.sqlite')
    source_model = os.path.join(current_dir, 'wine_application', 'XGB_unscaled_model.pkl')
    
    # Destination files
    dest_db = os.path.join(current_dir, 'wine_cellar.sqlite')
    dest_model = os.path.join(current_dir, 'XGB_unscaled_model.pkl')
    
    # Copy files if they don't exist
    if not os.path.exists(dest_db) and os.path.exists(source_db):
        shutil.copy2(source_db, dest_db)
        print(f"Copied {source_db} to {dest_db}")
    
    if not os.path.exists(dest_model) and os.path.exists(source_model):
        shutil.copy2(source_model, dest_model)
        print(f"Copied {source_model} to {dest_model}")

if __name__ == "__main__":
    setup_files()