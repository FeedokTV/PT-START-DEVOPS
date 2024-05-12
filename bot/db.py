import psycopg2
from psycopg2 import Error
import logging
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def init_db():
    connection = psycopg2.connect(user=os.environ['DB_USER'],
                                    password=os.environ['DB_PASSWORD'],
                                    host='db',
                                    port='5432', 
                                    database=os.environ['DB_DATABASE'])
    connection.autocommit = True
    logging.info('Connection to PostgreSQL - successful')
    cursor = connection.cursor()
    return cursor