from capture import Capture

from receivers.emailer import EmailReceiver


RECEIVER_CONTEXT = {
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
            capture.setup_receiver(EmailReceiver, RECEIVER_CONTEXT)
            capture.register_exception()


if __name__ == '__main__':
    TestOne.do()
