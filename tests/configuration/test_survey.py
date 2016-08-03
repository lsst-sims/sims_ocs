import unittest

from lsst.sims.ocs.configuration.survey import Survey

from tests.helpers import AREA_DIST_PROPS

class SurveyTest(unittest.TestCase):

    def setUp(self):
        self.survey = Survey()
        self.truth_start_date = "2022-01-01"

    def test_basic_information_from_creation(self):
        self.assertEqual(self.survey.start_date, self.truth_start_date)
        self.assertEqual(self.survey.duration, 1.0)
        self.assertEqual(self.survey.idle_delay, 60.0)
        self.assertEqual(self.survey.ad_proposals, AREA_DIST_PROPS)
