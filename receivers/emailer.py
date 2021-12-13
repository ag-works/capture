"""
Email Receiver class
"""

import os
import smtplib
import types
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailReceiver(object):
    """
    Receiver Class for sending text and html emails

    It accepts the recipients, subject, content
    """

    def __init__(self, host=None, port=None, user=None, password=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        if self.host is None and 'CAPTURE_EMAIL_HOST' in os.environ:
            self.host = os.environ['CAPTURE_EMAIL_HOST']
        if self.port is None and 'CAPTURE_EMAIL_PORT' in os.environ:
            self.port = os.environ['CAPTURE_EMAIL_PORT']
        if self.user is None and 'CAPTURE_EMAIL_USER' in os.environ:
            self.user = os.environ['CAPTURE_EMAIL_USER']
        if self.password is None and 'CAPTURE_EMAIL_PASSWORD' in os.environ:
            self.password = os.environ['CAPTURE_EMAIL_PASSWORD']

    def send_email(self, from_email, recipients, subject, content, is_html=False):
        message = EmailReceiver.prepare_message_object(from_email, recipients, subject, content,
                                                       is_html=is_html)

        connection = smtplib.SMTP(self.host, self.port)
        if self.user and self.password:
            connection.login(self.user, self.password)
        connection.sendmail(from_email, recipients, message.as_string())
        connection.quit()

    @staticmethod
    def prepare_message_object(from_email, recipients, subject, content, is_html=False):
        msg = MIMEMultipart()
        if isinstance(recipients, types.StringTypes):
            msg['To'] = recipients
        else:
            msg['To'] = ','.join(recipients)

        msg['From'] = from_email
        msg['Subject'] = subject
        html = MIMEText(content, 'html' if is_html is True else 'plain')
        msg.attach(html)
        return msg

    @staticmethod
    def send_exception(content, message, **kwargs):
        smtp_settings = dict()
        if 'smtp_settings' in kwargs:
            smtp_settings = kwargs['smtp_settings']

        assert 'from_email' in kwargs, "From address is mandatory for Email Receiver"
        assert 'recipients' in kwargs, "Recipients is mandatory for Email Receiver"

        email_sender = EmailReceiver(**smtp_settings)
        email_sender.send_email(kwargs['from_email'], kwargs['recipients'], message,
                                content, is_html=True)
