
import os, sys, socket, traceback

# third-party imports
from jinja2 import Environment, FileSystemLoader


class Capture(object):
    """
    Utility class to capture and compile the runtime exceptions

    This utility captures the exception and transforms it into HTML
    and reflecting more information than what we usually get while
    catching an exception, which could be very useful for debugging
    the code.

    sys.exc_info() => (type(exc_info), exc_info, exc_info.__traceback__)
    """

    def __init__(self, receiver_class=None, receiver_context=None):

        # Exception related properties
        self.exc_type = None
        self.exc_value = None
        self.exc_tb = None

        # HTML template related properties
        self.template_context = dict()

        # Receiver class and related properties
        self.receiver_class = receiver_class or ''
        self.receiver_context = receiver_context or ''

    @staticmethod
    def get_server_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def compile(self):
        stack = list()
        current_tb = self.exc_tb
        while current_tb is not None:
            lines = "".join(traceback.format_tb(current_tb, 1)).strip()
            local_values = current_tb.tb_frame.f_locals
            stack.append({'content': lines, 'locals': local_values})
            current_tb = current_tb.tb_next

        message = traceback.format_exception_only(self.exc_type, self.exc_value)
        message = "".join(message)
        self.template_context = {
            "server_ip": self.get_server_ip(),
            "stack": stack,
            "message": message,
        }

    def extend_template_context(self, **kwargs):
        self.template_context.update(kwargs)

    def extract_exception(self):
        exc_type, exc_value, exc_tb = sys.exc_info()
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb

    def setup_receiver(self, receiver_class, context):
        self.receiver_class = receiver_class
        self.receiver_context = context

    def get_content(self):
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = Environment(loader=FileSystemLoader(templates_path))
        template = jinja_env.get_template('alert.html')
        return template.render(**self.template_context)

    def register_exception(self):
        self.extract_exception()
        self.compile()
        self.extend_template_context()
        content = self.get_content()
        message = self.template_context['message']
        self.receiver_class.send_exception(content, message, **self.receiver_context)

