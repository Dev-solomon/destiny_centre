import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from main.middleware.email_template import order_template, payment_template # Assuming these functions are defined in EmailTemplates.py

EMAIL_SENDER = 'support@liziestyle.com'
EMAIL_PASS = 'dFsYEK66j9WV'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465  # Use port 465 for SMTP over SSL

def send_email(options):
    msg = MIMEMultipart()
    msg['From'] = options['from']
    msg['To'] = options['to']
    msg['Subject'] = options['subject']

    # Attach HTML content
    msg.attach(MIMEText(options['html'], 'html'))

    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASS)
            server.send_message(msg)
        print('Email sent')
    except Exception as e:
        print(f'Error: {e}')

def email_sender(email, subject, order):
    options = {
        'from': EMAIL_SENDER,
        'to': email,
        'subject': subject,
        'html': order_template(order) if order["status"] else ''
    }
    send_email(options)

def payment_email(subject, notice):
    options = {
        'from': EMAIL_SENDER,
        'to': EMAIL_SENDER,
        'subject': subject,
        'html': payment_template(notice) if notice["status"] else ''
    }
    send_email(options)
