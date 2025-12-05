import unittest
from pymixology.recommendation import suggester
from pymixology.inventory.items import Ingredient
from pymixology.exceptions import RecommendationError

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

        # Test partial matches / edge cases
        weird_recipes = [
            {
                "name": "Simple Drink",
                "ingredients": ["Rum"] # Simple string ingredient
            },
            {
                "name": "No Ingredients",
                "ingredients": []
            },
            {
                "name": "Free Drink",
                "ingredients": [{"name": "Air", "amount": None}] # No amount required
            }
        ]
        res = suggester.get_makeable_cocktails(self.inventory, weird_recipes)
        self.assertIn("Simple Drink", res)
        # "No Ingredients" has no ingredients, logic continues (returns empty normalized list), effectively skipped or considered not makeable in current logic?
        # Checking code: "if not normalized_ingredients: continue" -> so it won't be in the list
        self.assertNotIn("No Ingredients", res)
        # "Free Drink": "Air" is not in inventory, so it should fail even if amount is None?
        # Code: "inventory_item = inventory_lookup.get(name)" -> if not inventory_item: break
        self.assertNotIn("Free Drink", res)

        # Test Free Drink if we add Air
        self.inventory.append(Ingredient("Air", 100, "2099-01-01"))
        res_air = suggester.get_makeable_cocktails(self.inventory, weird_recipes)
        self.assertIn("Free Drink", res_air)

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
        
        # Test invalid profile
        bad_profile = {"sweet": -5}
        with self.assertRaises(RecommendationError):
            suggester.recommend_by_flavor(bad_profile, self.recipes)
        
        # Test surprise me
        # Mock random if needed, or just check it returns one of them
        surprise = suggester.surprise_me(self.recipes)
        names = [r["name"] for r in self.recipes]
        self.assertIn(surprise["name"], names)
        self.assertIsInstance(surprise, dict)
        
        # Test surprise me empty
        with self.assertRaises(RecommendationError):
            suggester.surprise_me([])

    def test_helpers(self):
        # Test internal helpers (specifically missing coverage for _ingredient_name)
        name_str = suggester._ingredient_name("Rum")
        self.assertEqual(name_str, "Rum")
        
        name_dict = suggester._ingredient_name({"name": "Gin", "amount": 10})
        self.assertEqual(name_dict, "Gin")

