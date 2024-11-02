import pandas as pd
from sqlalchemy import create_engine
import traceback

# Credentials
user = 'yellowbox_user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowbox_db'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')


files_to_import = {
    'data/CBE_credits.csv': 'credits',
    'data/CBE_movies_metadata.csv': 'movies',
    'data/CBE_ratings.csv': 'ratings',
    'data/CBE_disk.csv': 'disks',
    'data/CBE_users.csv': 'users',
    'data/CBE_orders.csv': 'orders',
    'data/CBE_kiosks.csv': 'kiosks'
}

for file_name, table_name in files_to_import.items():
    try:
        print(f"Importing {file_name} into {table_name}...")
        df = pd.read_csv(file_name)
        
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        print(f"Successfully imported {file_name} into {table_name}")
    except Exception as e:
        print(f"Error importing {file_name} into {table_name}: {e}")
        print(traceback.format_exc())
