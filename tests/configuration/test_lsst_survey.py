import unittest

from lsst.sims.ocs.configuration.lsst_survey import LsstSurvey

class LsstSurveyTest(unittest.TestCase):

    def setUp(self):
        self.survey = LsstSurvey()
        self.truth_start_date = "2020-05-24"

    def test_basic_information_from_creation(self):
        self.assertEqual(self.survey.start_date, self.truth_start_date)
        self.assertEqual(self.survey.duration, 1.0)
