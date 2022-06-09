from bookstore.settings import EMAIL_SMTP, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send__email(email_to_send_to, subject, body):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = EMAIL_HOST_USER
    message["To"] = email_to_send_to
    message["Subject"] = subject
    message["Bcc"] = email_to_send_to

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORT, context=context) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, email_to_send_to, text)

"""
using smtplib library and email.MIME we can send mails.
email.MIME is crucial, because when I tried to use
only smtplib it was sending the same mail twice
"""