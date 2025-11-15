import unittest
from scraper import scrape_mnc_jobs, scrape_gov_jobs, scrape_bank_jobs


class TestScrapers(unittest.TestCase):

    def test_mnc_list(self):
        data = scrape_mnc_jobs()
        self.assertIsInstance(data, list)

    def test_gov_list(self):
        data = scrape_gov_jobs()
        self.assertIsInstance(data, list)

    def test_bank_list(self):
        data = scrape_bank_jobs()
        self.assertIsInstance(data, list)
