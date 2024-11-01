import pandas as pd
from sqlalchemy import create_engine

# Database credentials
user = 'yellowbox_user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowbox_db'


engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# tables
df = pd.read_sql('SHOW TABLES;', con=engine)
print(df)
print()

# movies structure
df = pd.read_sql('DESCRIBE movies;', con=engine)
print(df)
print()

# movies data
df = pd.read_sql('SELECT * FROM movies LIMIT 5;', con=engine)
print(df)