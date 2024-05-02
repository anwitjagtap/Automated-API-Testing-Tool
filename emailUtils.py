from asyncore import read
from fileinput import filename
import os
from smtplib import SMTP
from email.message import EmailMessage
from email.mime.text import MIMEText

class Emailer:

    def __init__(self):
        self.sender_email = None
        self.sender_password = None
        self.to_emails = []
        self.subject = None
        self.cc = []
        self.bcc = []
        self.mailserver = SMTP("smtp.gmail.com", 587)
        self.message = EmailMessage()
        self.message.make_mixed()
        return
    
    def set_sender_email(self, email):
        self.sender_email = email
    
    def set_to_emails(self, email):
        self.to_emails = email

    def set_sender_password(self, password):
        self.sender_password = password
    
    def set_cc(self, cc):
        self.cc = cc

    def set_bcc(self, bcc):
        self.bcc = bcc
    
    def set_subject(self, subject):
        self.subject = subject
    
    def add_message_body(self, text):
        body = MIMEText(text, "plain")
        self.message.attach(body)

    def add_html(self, html):
        body = MIMEText(html, 'html')
        self.message.attach(body)

    def add_attachments(self, file, filename):
        with open(file, "r") as f:
            self.add_attachments(f.read(), filename = filename)

    def send_email(self):
        self.message['Subject'] = self.subject
        self.message['From'] = self.sender_email
        self.message['To'] = ", ".join(self.to_emails)
        self.message['CC'] = ", ".join(self.cc)
        self.mailserver.starttls()
        self.mailserver.login(self.sender_email, self.sender_password)
        self.mailserver.sendmail(self.sender_email, self.to_emails + self.cc + self.bcc, self.message.as_string())
        self.mailserver.quit()
    
