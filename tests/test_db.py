# tests/test_db.py
import unittest
import os
from utils import db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary DB file in the repo root for isolation
        self.temp_db = "test_jobs.db"
        db.init_db(db_path=self.temp_db)

    def test_insert_and_retrieve_job(self):
        test_job = {
            "title": "Software Engineer Intern",
            "company": "TestCorp",
            "link": "https://example.com/job",
            "last_date": "2025-11-30"
        }

        # Use compatibility wrapper save_job_if_new (returns True if inserted)
        inserted = db.save_job_if_new(test_job, db_path=self.temp_db)
        self.assertTrue(inserted, "Job should be inserted the first time")

        # Inserting again should return False (duplicate)
        inserted_again = db.save_job_if_new(test_job, db_path=self.temp_db)
        self.assertFalse(inserted_again, "Duplicate job should not be re-inserted")

    def tearDown(self):
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

if __name__ == "__main__":
    unittest.main()
