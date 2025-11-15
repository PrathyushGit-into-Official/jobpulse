import unittest
import os
from pathlib import Path
from utils import db


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_db = Path("test_jobs.db")
        if self.temp_db.exists():
            os.remove(self.temp_db)
        db.init_db(db_path=self.temp_db)

    def tearDown(self):
        if self.temp_db.exists():
            os.remove(self.temp_db)

    def test_insert_and_retrieve(self):
        job = {
            "title": "Software Engineer",
            "company": "TestCorp",
            "link": "https://example.com/job",
            "source": "test_source",
        }

        inserted = db.save_job_if_new(job, db_path=self.temp_db)
        self.assertTrue(inserted, "First insert should succeed")

        inserted_again = db.save_job_if_new(job, db_path=self.temp_db)
        self.assertFalse(inserted_again, "Duplicate job should be ignored")

        self.assertTrue(db.job_exists("https://example.com/job", db_path=self.temp_db))
