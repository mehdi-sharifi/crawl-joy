
import logging
import os
import psycopg2
from jobs import *
from init_env import *

logger = logging.getLogger(__name__)

# PostgreSQL database configuration
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = 5432
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

# Set up PostgreSQL connection
with psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
) as conn:
    create_car_ad_table(conn)
    create_user_notify_table(conn)
    sync_db(conn)
