import unittest
from utils import notifier


class TestNotifier(unittest.TestCase):

    def test_send_email_exists(self):
        self.assertTrue(callable(notifier.send_email))

    def test_send_telegram_exists(self):
        self.assertTrue(callable(notifier.send_telegram))

    def test_send_notification_exists(self):
        self.assertTrue(callable(notifier.send_notification))
