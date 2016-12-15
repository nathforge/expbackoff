import unittest

from expbackoff import Backoff

class FailuresPropertyTestCase(unittest.TestCase):
    def setUp(self):
        self.backoff = Backoff(0.5, 5)

    def test_set_to_zero(self):
        self.backoff.failures = 0
        self.assertEqual(self.backoff.failures, 0)

    def test_set_to_ten(self):
        self.backoff.failures = 10
        self.assertEqual(self.backoff.failures, 10)

    def test_fail_on_minus_one(self):
        with self.assertRaisesRegexp(ValueError, r"^Expected positive integer, received -1$"):
            self.backoff.failures = -1

    def test_fail_on_string(self):
        with self.assertRaisesRegexp(ValueError, r"^Expected positive integer, received '5'$"):
            self.backoff.failures = "5"

class GetRawSecondsTestCase(unittest.TestCase):
    def setUp(self):
        self.backoff = Backoff(0.5, 5)

    def test_with_zero_failures(self):
        self.backoff.failures = 0
        self.assertEqual(self.backoff._get_raw_seconds(), 0)

    def test_with_one_failures(self):
        self.backoff.failures = 1
        self.assertEqual(self.backoff._get_raw_seconds(), 0.5 * 2 ** 0)

    def test_with_two_failures(self):
        self.backoff.failures = 2
        self.assertEqual(self.backoff._get_raw_seconds(), 0.5 * 2 ** 1)

    def test_with_ten_failures(self):
        self.backoff.failures = 10
        self.assertEqual(self.backoff._get_raw_seconds(), self.backoff.max_seconds)

class UpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.backoff = Backoff(0.5, 5)

    def test_update(self):
        self.assertEqual(self.backoff.failures, 0)
        self.backoff.update(True);  self.assertEqual(self.backoff.failures, 0)
        self.backoff.update(True);  self.assertEqual(self.backoff.failures, 0)
        self.backoff.update(False); self.assertEqual(self.backoff.failures, 1)
        self.backoff.update(False); self.assertEqual(self.backoff.failures, 2)
        self.backoff.update(True);  self.assertEqual(self.backoff.failures, 1)
        self.backoff.update(True);  self.assertEqual(self.backoff.failures, 0)
        self.backoff.update(True);  self.assertEqual(self.backoff.failures, 0)
