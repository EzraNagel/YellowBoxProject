import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import Movie, Disk, User, Order, Kiosk, Rating  # Import models directly from app.models
import traceback
import numpy as np
from app import create_app

# Create the Flask app instance
app = create_app()

with app.app_context():
    db.create_all()

user = 'yellowbox_user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowbox_db'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
Session = sessionmaker(bind=engine)
session = Session()

files_to_import = {
    'data/CBE_movies_metadata.csv': Movie,
    'data/CBE_disk.csv': Disk,
    'data/CBE_users.csv': User,
    'data/CBE_orders.csv': Order,
    'data/CBE_kiosks.csv': Kiosk,
    'data/CBE_ratings.csv': Rating
}

# Function to map DataFrame to model fields
def map_to_model(df, model_class):
    model_data = []
    for _, row in df.iterrows():
        # Handle NaN (float) values
        row = row.apply(lambda value: None if isinstance(value, float) and np.isnan(value) else value)
        model_instance = model_class(**row.to_dict())
        model_data.append(model_instance)
    return model_data

# Import data for each file
for file_name, model_class in files_to_import.items():
    try:
        print(f"Importing {file_name} into {model_class.__name__}...")

        df = pd.read_csv(file_name)

        # Ensure NaN values are replaced with None for all float columns
        df = df.apply(lambda col: col.where(pd.notna(col), None) if col.dtype == 'float64' else col)

        model_data = map_to_model(df, model_class)

        # Add all rows to the session
        session.add_all(model_data)

        print(f"Successfully imported {file_name} into {model_class.__name__}")

    except Exception as e:
        print(f"Error importing {file_name} into {model_class.__name__}: {e}")
        print(traceback.format_exc())
        session.rollback()

# Commit after all files are processed
session.commit()
session.close()
