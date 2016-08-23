import unittest

from lsst.sims.ocs.environment import SeeingModel

class TestSeeingModel(unittest.TestCase):

    def setUp(self):
        self.seeing = SeeingModel()
        self.num_original_values = 210384

    def test_basic_information_after_creation(self):
        self.assertIsNone(self.seeing.seeing_db)
        self.assertIsNone(self.seeing.seeing_dates)
        self.assertIsNone(self.seeing.seeing_values)

    def test_information_after_initialization(self):
        self.seeing.initialize()
        self.assertEqual(self.seeing.seeing_values.size, self.num_original_values)
        self.assertEqual(self.seeing.seeing_dates.size, self.num_original_values)
