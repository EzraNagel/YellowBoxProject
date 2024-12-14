import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:yellowboxpassword$@yellowbox-db.c12ociym6hbt.us-east-1.rds.amazonaws.com:3306/yellowbox_db'