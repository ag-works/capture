
import traceback


class Capture(object):
    """
    Utility class to capture and compile the runtime exceptions

    This utility captures the exception and transforms it into HTML
    and reflecting more information than what we usually get while
    catching an exception, which could be very useful for debugging
    the code.

    type(exception), str(exception), exception.__traceback__ = sys.exc_info()
    """

    def __init__(self, adapter_class=None, adapter_context=None):

        # Exception related properties
        self.exc_type = None
        self.exc_value = None
        self.exc_tb = None

        # HTML notification template related properties
        self.custom_template = None
        self.template_context = dict()
        self.template_context_extras = None

        # Adapter class and related properties
        self.adapter_class = adapter_class or ''
        self.adapter_context = adapter_context or ''

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
            "stack": stack,
            "message": message,
        }

    def extend_template_context(self, **kwargs):
        self.template_context_extras = kwargs

    def extract(self, excp):
        """Method to extract the type, value and traceback of the exception"""
        self.exc_type = type(excp)
        self.exc_value = excp
        self.exc_tb = excp.__traceback__

    def set_adapter(self, adapter, context):
        self.adapter_class = adapter
        self.adapter_context = context

    def push(self, excp):
        if excp is None or not isinstance(excp, BaseException):
            assert "Object passed as an argument is not an Exception"

        self.extract(excp)
        self.compile()
        if self.template_context_extras is not None:
            self.template_context.update(self.template_context_extras)
        self.adapter_class.send_exception(self.template_context, **self.adapter_context)

