class Mail:
    def __init__(self):
        self.subject = ""
        self.to=[]
        self.from_user=""
        self.user_info=[]

    def send(self):
        print("Send to the user")
    
    def checkStatus(self):
        pass


# import os
# from celery import Celery
# from smtplib import SMTP_SSL
# from email.mime.text import MIMEText

# celery = Celery('tasks', broker='amqp://guest@localhost//')

# @celery.task
# def send_email(recipient_email):
#     email_password = os.environ.get("EMAIL_PASSWORD")
#     if not email_password:
#         raise ValueError("EMAIL_PASSWORD not set")

#     msg = MIMEText('This is a test email.')
#     msg['Subject'] = 'Test Email'
#     msg['From'] = 'akintola130@gmail.com'
#     msg['To'] = recipient_email

#     try:
#         with SMTP_SSL('smtp.gmail.com', 465) as server:
#             server.login('akintola130@gmail.com', email_password)
#             server.sendmail('akintola130@gmail.com', recipient_email, msg.as_string())
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")