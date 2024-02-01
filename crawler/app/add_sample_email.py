
import logging
import os
import psycopg2
from init_env import *

logger = logging.getLogger(__name__)

# PostgreSQL database configuration
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = 5432
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')


# Sample email addressess
sample_emails_address = os.environ.get('SAMPLE_EMAIL_ADDRESS')
sample_emails = [sample_emails_address]

try:
    # Set up PostgreSQL connection
    with psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    ) as conn:
        create_user_notify_table(conn)
        import_sample_emails(conn, sample_emails)

except psycopg2.Error as e:
    logger.error(f"PostgreSQL error: {str(e)}")

except Exception as e:
    logger.error(f"An unexpected error occurred: {str(e)}")

