import unittest
from pymixology.inventory.items import Ingredient, Spirit, Mixer

class TestItems(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.base_value = 10.0
        cls.base_quantity = 100.0

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.ingredient = Ingredient("Sugar", 100.0, "2025-12-31", value=10.0)
        self.spirit = Spirit("Vodka", 750.0, "2030-01-01", abv=40.0, value=20.0)
        self.mixer = Mixer("Soda", 330.0, "2024-06-01", is_carbonated=True, value=2.0)

    def tearDown(self):
        del self.ingredient
        del self.spirit
        del self.mixer

    def test_ingredient_methods(self):
        # Test 1: Initial value check
        self.assertEqual(self.ingredient.name, "Sugar")
        self.assertEqual(self.ingredient.quantity, 100.0)
        self.assertEqual(self.ingredient.current_value(), 10.0)
        
        # Test 2: use() method valid
        success = self.ingredient.use(50.0)
        self.assertTrue(success)
        self.assertEqual(self.ingredient.quantity, 50.0)
        self.assertEqual(self.ingredient.current_value(), 5.0)

        # Test 3: use() method invalid (too much)
        fail_success = self.ingredient.use(1000.0)
        self.assertFalse(fail_success)
        self.assertEqual(self.ingredient.quantity, 50.0)
        
        # Test 4: use() method invalid (negative)
        neg_success = self.ingredient.use(-10.0)
        self.assertFalse(neg_success)
        
        # Additional check for info string
        self.assertIn("Sugar", self.ingredient.info())
        self.assertIn("Qty: 50.0", self.ingredient.info())

    def test_spirit_and_mixer(self):
        # Test Spirit specific
        self.assertEqual(self.spirit.name, "Vodka")
        self.assertEqual(self.spirit.get_abv(), 40.0)
        self.assertIsInstance(self.spirit, Ingredient)
        self.assertTrue(self.spirit.use(10.0))
        
        # Test Mixer specific
        self.assertEqual(self.mixer.name, "Soda")
        self.assertTrue(self.mixer.is_fizzy())
        self.assertIsInstance(self.mixer, Ingredient)
        self.assertEqual(self.mixer.unit_value, 2.0/330.0)
        
        # Verify inheritance logic works for value calculation
        original_val = self.spirit.current_value() # (20.0/750.0) * 740.0
        expected = (20.0/750.0) * 740.0
        self.assertAlmostEqual(original_val, expected)

