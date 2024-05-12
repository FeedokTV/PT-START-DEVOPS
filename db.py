import psycopg2
from psycopg2 import Error
import logging
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def init_db():
    connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                    password=os.getenv('DB_PASSWORD'),
                                    host=os.getenv('DB_HOST'),
                                    port=os.getenv('DB_POST'), 
                                    database=os.getenv('DB_DATABASE'))
    connection.autocommit = True
    logging.info('Connection to PostgreSQL - successful')
    cursor = connection.cursor()
    return cursor