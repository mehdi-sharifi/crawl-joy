import logging, redis, os, json
import psycopg2
from psycopg2 import sql
from crawler import fetch_from_bama
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = 5432
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = 6379


def sync_db(conn):
    try:
        logger.info('Starting data transfer from Redis to database...')

        # Connect to Redis and get all keys
        cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        keys = cache.keys()

        # Transfer each car ad from Redis to PostgreSQL
        for key in keys:
            ad_data = cache.get(key)
            if ad_data:
                ad_data = json.loads(ad_data.decode('utf-8'))
                values = (
                    ad_data["code"],
                    ad_data["url"],
                    ad_data["title"],
                    ad_data["price"],
                    ad_data["year"],
                    ad_data["mileage"],
                    ad_data["color"],
                    ad_data["body_status"],
                    ad_data["modified_date"],
                )
                save_car_ad(conn, values)

        logger.info('Data transfer complete.')
    except Exception as e:
        logger.error(f"An error occurred during data transfer: {e}", exc_info=True)


def save_car_ad(conn, values):
    try:
        # Save to PostgreSQL
        with conn.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO car_ad (code, url, title, price, year, mileage, color, body_status, modified_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO NOTHING;
            """)
            cursor.execute(insert_query, values)
        conn.commit()
        logger.info(f"Car ad saved to PostgreSQL: {values[0]}")

        # Save to Redis
        ad_key = values[0]  # Assuming 'code' is the key for the ad in Redis
        ad_data = {
            "code": values[0],
            "url": values[1],
            "title": values[2],
            "price": values[3],
            "year": values[4],
            "mileage": values[5],
            "color": values[6],
            "body_status": values[7],
            "modified_date": values[8],  # Convert datetime to ISO format
        }
        ad_cache=redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        ad_cache.set(ad_key, json.dumps(ad_data).encode('utf-8'))
        logger.info(f"Car ad saved to Redis: {values[0]}")
    except Exception as e:
        logger.error(f"Error saving car ad: {e}", exc_info=True)


def send_email_async(state, url, title, year, mileage, price, recipients):
    try:
        # Your email and password
        email_address = EMAIL_HOST_USER
        email_password = EMAIL_HOST_PASSWORD

        # SMTP server settings (replace with your email provider's SMTP server and port)
        smtp_server = EMAIL_HOST
        smtp_port = 587

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipients
        msg['Subject'] = f'New Car Ads in {state}'

        # Attach body to the message
        body = f'{title}\n سال ساخت:{year}\n کارکرد:{mileage}\n قیمت:{price}\n click here to jump in this ad:\n https://bama.ir{url}'

        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS for security
            server.starttls()

            # Login to the email account
            server.login(email_address, email_password)

            # Send the email
            server.sendmail(email_address, recipients, msg.as_string())

        logger.info('Email sent successfully!')
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")

def crawl_bama_ads(state):
    try:
        logger.info(f"Starting Bama ads crawl for state: {state}")
        # Set up PostgreSQL connection
        with psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        ) as conn:

            car_ad = fetch_from_bama(state)
            ad_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
            user_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)

            # Fetch user emails from Redis or database if not cached
            recipients_key = 'user_emails'
            recipients = user_cache.get(recipients_key)

            if recipients is None:
                # Simulate fetching user emails from PostgreSQL
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_email FROM user_notify;")
                    recipients = [row[0] for row in cursor.fetchall()]

                # Store user emails in Redis with expiration (e.g., 1 hour)
                    user_cache.set(recipients_key, json.dumps(recipients).encode('utf-8'), ex=3600)
            else:
                recipients = json.loads(recipients.decode('utf-8'))

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
                    save_car_ad(conn, values,)
                    send_email_async(state, value["url"], value["title"], value["year"], value["mileage"], value["price"], "sharifi.mehdi1995@gmail.com")

            if not_exist > 0:
                logger.error(f'{not_exist} of Codes do not exist in the database.')
            else:
                logger.info(f'No new ads for state {state}')
    except Exception as e:
        logger.error(f"An error occurred in Bama ads crawl: {e}", exc_info=True)
