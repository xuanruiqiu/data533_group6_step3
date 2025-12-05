import unittest
import json
import os
import tempfile
from pymixology.recipes import catalog

class TestCatalog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary file with dummy recipe data
        cls.test_data = [
            {
                "name": "Test Mojito",
                "base": "Rum",
                "ingredients": [
                    {"name": "Rum", "amount": 60, "unit": "ml"},
                    {"name": "Mint", "amount": 6, "unit": "leaves"}
                ],
                "steps": ["Muddle mint", "Add rum", "Top with soda"]
            },
            {
                "name": "Test Martini",
                "base": "Gin",
                "ingredients": [
                    {"name": "Gin", "amount": 60, "unit": "ml"},
                    {"name": "Vermouth", "amount": 10, "unit": "ml"}
                ],
                "steps": ["Stir", "Strain"]
            }
        ]
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump(cls.test_data, cls.temp_file)
        cls.temp_file.close()

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.temp_file.name)

    def setUp(self):
        self.recipes = catalog.load_recipes(self.temp_file.name)

    def tearDown(self):
        self.recipes = []

    def test_load_search(self):
        # Test loading
        self.assertEqual(len(self.recipes), 2)
        self.assertEqual(self.recipes[0]["name"], "Test Mojito")
        
        # Test search valid
        results = catalog.search_cocktail(self.recipes, "mojito")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Test Mojito")
        
        # Test search invalid
        results_none = catalog.search_cocktail(self.recipes, "Whiskey")
        self.assertEqual(len(results_none), 0)
        
        # Test search partial
        results_part = catalog.search_cocktail(self.recipes, "Test")
        self.assertEqual(len(results_part), 2)

    def test_filter_and_helpers(self):
        # Test filter_by_base
        rum_drinks = catalog.filter_by_base(self.recipes, "Rum")
        self.assertEqual(len(rum_drinks), 1)
        self.assertEqual(rum_drinks[0]["name"], "Test Mojito")
        
        gin_drinks = catalog.filter_by_base(self.recipes, "gin") # case insensitive
        self.assertEqual(len(gin_drinks), 1)
        
        # Test normalize helper (indirectly via load)
        ing = self.recipes[0]["ingredients"][0]
        self.assertIn("name", ing)
        self.assertIn("amount", ing)
        self.assertIn("unit", ing)
        
        # Test format ingredient string helper
        # Note: _format_ingredient is not exported in __all__ usually, but accessible in Python
        # Testing it via display logic or direct access if possible. 
        # Let's test direct access since it's a unit test.
        fmt = catalog._format_ingredient({"name": "Lime", "amount": 1, "unit": "wedge"})
        self.assertIn("1", fmt)
        self.assertIn("wedge", fmt)
        self.assertIn("Lime", fmt)

