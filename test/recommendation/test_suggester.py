import unittest
from pymixology.recommendation import suggester
from pymixology.inventory.items import Ingredient

class TestSuggester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.inventory = [
            Ingredient("Rum", 1000, "2025-01-01"),
            Ingredient("Mint", 50, "2024-01-01"),
            Ingredient("Lime", 10, "2024-01-01"),
            Ingredient("Sugar", 500, "2025-01-01")
        ]
        self.recipes = [
            {
                "name": "Mojito",
                "ingredients": [
                    {"name": "Rum", "amount": 60},
                    {"name": "Mint", "amount": 10},
                    {"name": "Lime", "amount": 1},
                    {"name": "Sugar", "amount": 10}
                ],
                "flavor": "sweet"
            },
            {
                "name": "Daiquiri",
                "ingredients": [
                    {"name": "Rum", "amount": 60},
                    {"name": "Lime", "amount": 1},
                    {"name": "Sugar", "amount": 10}
                ],
                "flavor": "sour"
            },
            {
                "name": "Impossible Drink",
                "ingredients": [
                    {"name": "Unicorn Tears", "amount": 10}
                ],
                "flavor": "bitter"
            }
        ]
        self.profile = {"sweet": 5, "sour": 3, "bitter": 1}

    def tearDown(self):
        pass

    def test_makeable(self):
        # Test makeable logic
        makeable = suggester.get_makeable_cocktails(self.inventory, self.recipes)
        self.assertIn("Mojito", makeable)
        self.assertIn("Daiquiri", makeable)
        self.assertNotIn("Impossible Drink", makeable)
        self.assertEqual(len(makeable), 2)

    def test_recommendations(self):
        # Test find by ingredient
        matches = suggester.find_cocktails_with_ingredients(["Mint"], self.recipes)
        self.assertIn("Mojito", matches)
        self.assertNotIn("Daiquiri", matches)
        
        # Test flavor recommendation
        recs = suggester.recommend_by_flavor(self.profile, self.recipes)
        # Sweet (5) > Sour (3) > Bitter (1)
        self.assertEqual(recs[0], "Mojito")
        self.assertEqual(recs[1], "Daiquiri")
        self.assertEqual(recs[2], "Impossible Drink")
        
        # Test surprise me
        # Mock random if needed, or just check it returns one of them
        surprise = suggester.surprise_me(self.recipes)
        names = [r["name"] for r in self.recipes]
        self.assertIn(surprise["name"], names)
        self.assertIsInstance(surprise, dict)

