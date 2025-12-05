import unittest
from pymixology.recipes import tools

class TestTools(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.oz_ml_factor = 29.5735

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.ingredients_abv = [
            {"vol": 60, "abv": 40}, # 2400
            {"vol": 30, "abv": 0}   # 0
        ] # total vol 90, total alc 2400 -> 26.66...
        self.ingredients_cost = [
            {"bottle_vol": 1000, "price_per_bottle": 100, "used_vol": 50}, # 5.0
            {"bottle_vol": 500, "price_per_bottle": 10, "used_vol": 50}   # 1.0
        ]

    def tearDown(self):
        pass

    def test_conversions(self):
        # Test oz to ml
        res_ml = tools.unit_converter(1, "oz", "ml")
        self.assertAlmostEqual(res_ml, self.oz_ml_factor)
        
        # Test ml to oz
        res_oz = tools.unit_converter(self.oz_ml_factor, "ml", "oz")
        self.assertAlmostEqual(res_oz, 1.0)
        
        # Test same unit
        res_same = tools.unit_converter(10, "ml", "ml")
        self.assertEqual(res_same, 10)
        
        # Test invalid unit
        with self.assertRaises(ValueError):
            tools.unit_converter(10, "gal", "ml")

    def test_calculations(self):
        # Test ABV
        abv = tools.calculate_abv(self.ingredients_abv)
        self.assertAlmostEqual(abv, 26.6666666, places=2)
        
        # Test Cost
        cost = tools.estimate_cost(self.ingredients_cost)
        self.assertAlmostEqual(cost, 6.0)
        
        # Test Scale Recipe
        recipe = {
            "name": "Test",
            "servings": 1,
            "ingredients": [{"name": "Gin", "amount": 60}]
        }
        scaled = tools.scale_recipe(recipe, 2)
        self.assertEqual(scaled["servings"], 2)
        self.assertEqual(scaled["ingredients"][0]["amount"], 120)
        
        # Test Scale Invalid
        with self.assertRaises(ValueError):
            tools.scale_recipe(recipe, -1)

