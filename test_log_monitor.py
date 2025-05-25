import unittest
import logging
import io

import log_monitor

class TestLogMonitor(unittest.TestCase):
    # Executes before tests
    def setUp(self):
        # Capture logs with a dedicated handler
        self.log_output = io.StringIO()
        self.log_handler = logging.StreamHandler(self.log_output)
        self.log_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

        self.logger = logging.getLogger()
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)

    # Executes after tests
    def tearDown(self):
        self.logger.removeHandler(self.log_handler)
        self.log_handler.close()
        self.log_output.close()

    # Runs the main method (analyze_logs) with mocked CSV data
    def run_analyzer_with_csv(self, csv_content):
        csv_file = io.StringIO(csv_content)
        log_monitor.analyze_logs(csv_file)
        return self.log_output.getvalue()

    # Tests the normal case, when no ERROR/WARNING log is printed
    # i.e. tasks are all below 5 minutes
    def test_normal_duration(self):
        csv_data =  """11:00:00,desc, START,1001
11:04:00,desc, END,1001
"""
        output = self.run_analyzer_with_csv(csv_data)
        self.assertNotIn("ERROR", output)
        self.assertNotIn("WARNING", output)

    # Tests a case when a task longer than 5 minutes exists,
    # so we must print a WARNING
    def test_warning_duration(self):
        csv_data = """11:00:00,desc, START,1002
11:06:00,desc, END,1002
"""
        output = self.run_analyzer_with_csv(csv_data)
        self.assertIn("WARNING", output)

    # Tests a case when a task longer than 10 minutes exists in the logs,
    # so we must print an ERROR
    def test_error_duration(self):
        csv_data = """11:00:00,desc, START,1003
11:15:00,desc, END,1003
"""
        output = self.run_analyzer_with_csv(csv_data)
        self.assertIn("ERROR", output)
        self.assertIn("1003", output)

    # tests a malformed CSV case, when we have an END event without a START event for a task-id
    def test_end_without_start(self):
        csv_data = """11:20:00,desc, END,1004"""
        output = self.run_analyzer_with_csv(csv_data)
        self.assertIn("ERROR", output)
        self.assertIn("no corresponding START", output)

    # tests a CSV with a row containing more or lest than 4 elements
    def test_malformed_row_skipped(self):
        csv_data = """11:20:00,desc, START
11:25:00,desc, END,1005
"""
        output = self.run_analyzer_with_csv(csv_data)
        self.assertIn("no corresponding START", output)

if __name__ == '__main__':
    unittest.main()
