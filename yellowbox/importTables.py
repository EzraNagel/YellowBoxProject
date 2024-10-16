import pandas as pd
from sqlalchemy import create_engine
import json

user = 'user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowboxdb'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

credits_file_name = 'yellowbox/data/CBE_credits.csv'
df = pd.read_csv(credits_file_name)

df.to_sql('credits', con=engine, if_exists='replace', index=False)

credits_file_name = 'yellowbox\data\CBE_movies_metadata.csv'
df = pd.read_csv(credits_file_name)

df.to_sql('movies', con=engine, if_exists='replace', index=False)

credits_file_name = 'yellowbox\data\CBE_ratings.csv'
df = pd.read_csv(credits_file_name)

df.to_sql('ratings', con=engine, if_exists='replace', index=False)
