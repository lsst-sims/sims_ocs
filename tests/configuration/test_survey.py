import unittest

from lsst.sims.ocs.configuration.survey import Survey
from tests.helpers import NUM_AREA_DIST_PROPS

class SurveyTest(unittest.TestCase):

    def setUp(self):
        self.survey = Survey()
        self.truth_start_date = "2022-01-01"

    def test_basic_information_from_creation(self):
        self.assertEqual(self.survey.start_date, self.truth_start_date)
        self.assertEqual(self.survey.duration, 1.0)
        self.assertIsNotNone(self.survey.area_dist_props)
        self.assertEqual(len(self.survey.area_dist_props), NUM_AREA_DIST_PROPS)
