import redis
import logging
import os
from crawler import fetch_from_bama
from jobs import save_car_ad

logger = logging.getLogger(__name__)

# PostgreSQL database configuration
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = 5432
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = 6379


def create_car_ad_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS car_ad (
                code VARCHAR(100) PRIMARY KEY,
                url VARCHAR(255),
                title VARCHAR(255),
                price VARCHAR(20),
                year VARCHAR(4),
                mileage VARCHAR(20),
                color VARCHAR(50),
                body_status VARCHAR(50),
                modified_date TIMESTAMP
            );
        """)
    conn.commit()
    
def create_user_notify_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_notify (
                    user_email VARCHAR(255) PRIMARY KEY
                );
            """)
        conn.commit()
        logger.info("user_notify table created successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating user_notify table: {str(e)}")

def deploy(state, conn):
    try:
        logger.info(f"Starting Bama ads crawl for state: {state}")
        car_ad = fetch_from_bama(state)
        ad_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        not_exist = 0
        for key, value in car_ad.items():
            if not ad_cache.exists(key):
                not_exist += 1
                values = (
                    value["code"],
                    value["url"],
                    value["title"],
                    value["price"],
                    value["year"],
                    value["mileage"],
                    value["color"],
                    value["body_status"],
                    value["modified_date"],
                )
                save_car_ad(conn, values)
        if not_exist > 0:
            logger.error(f'{not_exist} of Codes do not exist in the database.')
        else:
            logger.info(f'No new ads for state {state}')
    except Exception as e:
        logger.error(f"An error occurred in Bama ads crawl: {e}", exc_info=True)

def import_sample_emails(conn, sample_emails):
    try:
        with conn.cursor() as cursor:
            insert_query = "INSERT INTO user_notify (user_email) VALUES (%s) ON CONFLICT (user_email) DO NOTHING;"
            cursor.executemany(insert_query, [(email,) for email in sample_emails])
        conn.commit()
        logger.info("Sample emails imported successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error importing sample emails: {str(e)}")