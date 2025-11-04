# tests/test_notifier.py
import unittest
from utils import notifier

class TestNotifier(unittest.TestCase):
    def test_send_email_function_exists(self):
        self.assertTrue(callable(getattr(notifier, "send_email", None)))

    def test_send_telegram_function_exists(self):
        self.assertTrue(callable(getattr(notifier, "send_telegram", None)))

    def test_send_notification_function_exists(self):
        self.assertTrue(callable(getattr(notifier, "send_notification", None)))

if __name__ == "__main__":
    unittest.main()
