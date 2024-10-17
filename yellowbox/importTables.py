import pandas as pd
from sqlalchemy import create_engine
import json


# Credentials depend on how you set up the database
user = 'yellowbox_user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowbox_db'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

credits_file_name = 'data/CBE_credits.csv'
df = pd.read_csv(credits_file_name)

df.to_sql('credits', con=engine, if_exists='replace', index=False)

credits_file_name = 'data/CBE_movies_metadata.csv'
df = pd.read_csv(credits_file_name)

df.to_sql('movies', con=engine, if_exists='replace', index=False)

credits_file_name = 'data/CBE_ratings.csv'
df = pd.read_csv(credits_file_name)

df.to_sql('ratings', con=engine, if_exists='replace', index=False)

disks_file_name = 'data/CBE_disk.csv'
df = pd.read_csv(disks_file_name)

df.to_sql('disks', con=engine, if_exists='replace', index=False)

users_file_name = 'data/CBE_users.csv'
df = pd.read_csv(users_file_name)

df.to_sql('users', con=engine, if_exists='replace', index=False)

orders_file_name = 'data/CBE_orders.csv'
df = pd.read_csv(orders_file_name)

df.to_sql('orders', con=engine, if_exists='replace', index=False)
