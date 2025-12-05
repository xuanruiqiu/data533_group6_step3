import unittest
from pymixology.inventory.items import Ingredient, Spirit
from pymixology.inventory import manager

class TestManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_inventory_name = "Test Bar"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.inventory = []
        self.item1 = Ingredient("Lemon", 10.0, "2024-01-01", value=5.0)
        self.item2 = Spirit("Gin", 700.0, "2025-01-01", abv=40.0, value=30.0)
        manager.add_item(self.inventory, self.item1)

    def tearDown(self):
        self.inventory = []

    def test_add_remove(self):
        # Test Add
        initial_len = len(self.inventory)
        manager.add_item(self.inventory, self.item2)
        self.assertEqual(len(self.inventory), initial_len + 1)
        self.assertIn(self.item2, self.inventory)
        
        # Test Add Invalid
        with self.assertRaises(TypeError):
            manager.add_item(self.inventory, "Not an Ingredient")
        
        # Test Remove Existing
        removed = manager.remove_item(self.inventory, "Lemon")
        self.assertTrue(removed)
        self.assertEqual(len(self.inventory), 1)
        
        # Test Remove Non-existing
        removed_fail = manager.remove_item(self.inventory, "Gold")
        self.assertFalse(removed_fail)
        self.assertEqual(len(self.inventory), 1)

    def test_stock_logic(self):
        manager.add_item(self.inventory, self.item2)
        
        # Test check_stock
        qty = manager.check_stock(self.inventory, "Gin")
        self.assertEqual(qty, 700.0)
        qty_missing = manager.check_stock(self.inventory, "Missing")
        self.assertEqual(qty_missing, 0.0)
        
        # Test total_value
        # Lemon (5.0) + Gin (30.0) = 35.0
        self.assertAlmostEqual(manager.total_value(self.inventory), 35.0)
        
        # Test get_shopping_list
        # Lemon has 10.0, let's say threshold is 20.0 -> should be in list
        shopping = manager.get_shopping_list(self.inventory, 20.0)
        self.assertIn("Lemon", shopping)
        # Gin has 700.0, threshold 20.0 -> should not be in list
        self.assertNotIn("Gin", shopping)
        
        # Update Lemon to be 0
        self.inventory[0].use(10.0)
        self.assertAlmostEqual(self.inventory[0].quantity, 0.0)
        self.assertAlmostEqual(manager.total_value(self.inventory), 30.0)

