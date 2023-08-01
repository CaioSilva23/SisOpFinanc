import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config


# Configurações do servidor de e-mail
email_host = config('email_host', str)
email_port = config('email_port', int)
email_user = config('email_user', str)
email_password = config('email_password', str)


def create_message(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg


def send_mail(to_email=None, subject=None, body=None):
    try:
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()

        server.login(email_user, email_password)

        msg = create_message(to_email=to_email, subject=subject, body=body)

        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False
