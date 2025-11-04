# tests/test_scrapers.py
import unittest
from scraper import mnc_scraper, gov_scraper, bank_scraper

class TestScrapers(unittest.TestCase):
    def test_mnc_scraper_returns_list(self):
        data = mnc_scraper.scrape_mnc_jobs()
        self.assertIsInstance(data, list)

    def test_gov_scraper_returns_list(self):
        data = gov_scraper.scrape_gov_jobs()
        self.assertIsInstance(data, list)

    def test_bank_scraper_returns_list(self):
        data = bank_scraper.scrape_bank_jobs()
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
