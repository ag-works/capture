"""
Email Adapter class
"""
from __future__ import absolute_import

from capture.adapters.base import BaseAdapter

import os
import sys
import smtplib
import types
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.version_info.major == 2:
    StringTypes = types.StringTypes
else:
    StringTypes = (str,)

# Dependency imports
try:
    from jinja2 import Environment, FileSystemLoader
except:
    print("Failed to import dependency module jinja2! Please install jinja2 package")
    sys.exit(1)


class EmailAdapter(BaseAdapter):
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

    @staticmethod
    def get_content(context):
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        jinja_env = Environment(loader=FileSystemLoader(templates_path))
        template = jinja_env.get_template('alert.html')
        return template.render(**context)

    def send_email(self, from_email, recipients, subject, content, is_html=False):
        message = self.prepare_message_object(from_email, recipients, subject, content,
                                              is_html=is_html)

        connection = smtplib.SMTP(self.host, self.port)
        if self.user and self.password:
            connection.login(self.user, self.password)
        connection.sendmail(from_email, recipients, message.as_string())
        connection.quit()

    @staticmethod
    def prepare_message_object(from_email, recipients, subject, content, is_html=False):
        msg = MIMEMultipart()
        if isinstance(recipients, StringTypes):
            msg['To'] = recipients
        else:
            msg['To'] = ','.join(recipients)

        msg['From'] = from_email
        msg['Subject'] = subject
        html = MIMEText(content, 'html' if is_html is True else 'plain')
        msg.attach(html)
        return msg

    @staticmethod
    def send_exception(context, **kwargs):
        smtp_settings = dict()
        if 'smtp_settings' in kwargs:
            smtp_settings = kwargs['smtp_settings']

        assert 'from_email' in kwargs, "From address is mandatory for Email Adapter"
        assert 'recipients' in kwargs, "Recipients is mandatory for Email Adapter"

        subject = context['message']
        content = EmailAdapter.get_content(context)
        email_sender = EmailAdapter(**smtp_settings)
        email_sender.send_email(kwargs['from_email'], kwargs['recipients'], subject,
                                content, is_html=True)
