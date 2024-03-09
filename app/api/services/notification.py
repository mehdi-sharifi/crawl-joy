
import logging, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_host = os.environ.get('EMAIL_HOST')
email_port = 587
email_use_tls = True
email_host_user = os.environ.get('EMAIL_HOST_USER')
email_host_password = os.environ.get('EMAIL_HOST_PASSWORD')

logger = logging.getLogger(__name__)


def send_email(state, url, title, year, mileage, price, recipients):
    try:
        # Your email and password
        email_address = email_host_user
        email_password = email_host_password

        # SMTP server settings (replace with your email provider's SMTP server and port)
        smtp_server = email_host
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

        logger.info(f'Email sent successfully! for ads: {title} ')
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")