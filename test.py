from capture import Capture

from adapters.emailer import EmailAdapter


EMAIL_ADAPTER_PROPERTIES = {
    'from_email': '<email-address>',
    'recipients': '<email-address>',
}


class TestOne(object):
    """
    Test-case suite
    """

    @classmethod
    def divide(cls, x, y):
        return cls.divide(x//y, y-1)

    @staticmethod
    def do():
        try:
            TestOne.divide(10000, 8)
        except:
            capture = Capture()
            capture.setup_receiver(EmailAdapter, EMAIL_ADAPTER_PROPERTIES)
            capture.register_exception()


if __name__ == '__main__':
    TestOne.do()
