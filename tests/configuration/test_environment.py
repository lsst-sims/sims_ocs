import unittest

from lsst.sims.ocs.configuration.environment import Environment

class EnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.environ = Environment()

    def test_basic_information_after_creation(self):
        self.assertEqual(self.environ.seeing_db, "")
        self.assertEqual(self.environ.cloud_db, "")
