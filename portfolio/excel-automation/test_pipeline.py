import tempfile,unittest
from pathlib import Path
from pipeline import BASE,run
class Tests(unittest.TestCase):
    def test_valid(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(BASE/'data'/'sales.csv',Path(d)/'report.xlsx'),(4,0))
    def test_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(BASE/'data'/'sales_invalid.csv',Path(d)/'report.xlsx'),(1,2))
if __name__=='__main__':unittest.main()
