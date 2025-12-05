import unittest
from pymixology.recommendation import preference

class TestPreference(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Reset global profile just in case
        preference.user_profile = {}
        self.reviews_list = []
        self.reviews_dict = {}

    def tearDown(self):
        preference.user_profile = {}

    def test_profile(self):
        # Test set profile
        prof = preference.set_flavor_profile(5, 4, 3, 2)
        self.assertEqual(prof["sweet"], 5)
        self.assertEqual(prof["sour"], 4)
        self.assertEqual(prof["bitter"], 3)
        self.assertEqual(prof["strong"], 2)
        
        # Check global state update
        self.assertEqual(preference.user_profile["sweet"], 5)

    def test_reviews(self):
        # Test record list
        preference.record_review(self.reviews_list, "Mojito", 5)
        preference.record_review(self.reviews_list, "Negroni", 4)
        self.assertEqual(len(self.reviews_list), 2)
        self.assertEqual(self.reviews_list[0]["rating"], 5)
        
        # Test record dict
        preference.record_review(self.reviews_dict, "Mojito", 5)
        self.assertEqual(self.reviews_dict["Mojito"], 5)
        
        # Test top favorites
        preference.record_review(self.reviews_list, "Bad Drink", 1)
        top = preference.get_top_favorites(self.reviews_list, top_n=2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0], "Mojito")
        self.assertNotIn("Bad Drink", top)

