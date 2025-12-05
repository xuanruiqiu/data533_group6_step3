import unittest
import sys
import os

# Ensure the project root is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.liu.day1.test_items import TestItems
from tests.liu.day2.test_manager import TestManager
from tests.yang.day1.test_catalog import TestCatalog
from tests.yang.day2.test_tools import TestTools
from tests.qiu.day1.test_preference import TestPreference
from tests.qiu.day2.test_suggester import TestSuggester

def my_suite():
    suite = unittest.TestSuite()
    
    # Add tests from all classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestItems))
    suite.addTests(loader.loadTestsFromTestCase(TestManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCatalog))
    suite.addTests(loader.loadTestsFromTestCase(TestTools))
    suite.addTests(loader.loadTestsFromTestCase(TestPreference))
    suite.addTests(loader.loadTestsFromTestCase(TestSuggester))
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(my_suite())
    if not result.wasSuccessful():
        sys.exit(1)
