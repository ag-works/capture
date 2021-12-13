import smtplib
import types
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailSender(object):
    """
    Class for sending text and html emails along with the attachments

    It accepts the recipients subject, content and attachment
    file paths.
    """

    def __init__(self, hostname=None, port=25, username='', password=''):
        self._connection = smtplib.SMTP()
        self._connection.connect(hostname, port)
        self._connection.login(username, password)

    def send_email(self, from_email, recipients, subject, content, is_html=False,
                   attachments=tuple()):

        msg = MIMEMultipart()
        if isinstance(recipients, types.StringTypes):
            msg['To'] = recipients
        else:
            msg['To'] = ','.join(recipients)

        msg['From'] = from_email
        msg['Subject'] = subject
        html = MIMEText(content, 'html' if is_html else 'plain')
        msg.attach(html)
        self.add_attachments(msg, attachments)
        self._connection.sendmail(from_email, recipients, msg.as_string())

    @staticmethod
    def add_attachments(message, attachments):
        """
        Method to add the attachments to the given email message
        """

        for attachment in attachments:
            try:
                with open(attachment, 'rb') as file:
                    filecontent = file.read()
                    filename = os.path.basename(attachment)
            except Exception as e:
                print e
            else:
                payload = MIMEBase('application', 'octet-stream')
                payload.set_payload(filecontent)
                encoders.encode_base64(payload)
                payload.add_header("Content-Disposition", "attachment",
                                   filename=filename)
                message.attach(payload)

    def close_connection(self):
        """Method to close the SMTP connection"""
        self._connection.quit()
