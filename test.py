from capture import Capture

from capture.adapters.email import EmailAdapter


capture = Capture()
EMAIL_ADAPTER_PROPERTIES = {
    'from_email': '<email-address>',
    'recipients': '<email-address>',
}
capture.set_adapter(EmailAdapter, EMAIL_ADAPTER_PROPERTIES)


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
        except Exception as ex:
            capture.push(ex)


if __name__ == '__main__':
    TestOne.do()
