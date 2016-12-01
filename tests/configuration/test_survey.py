import unittest

from lsst.sims.ocs.configuration.survey import Survey

from tests.helpers import GEN_PROPS

class SurveyTest(unittest.TestCase):

    def setUp(self):
        self.survey = Survey()
        self.truth_start_date = "2022-01-01"

    def test_basic_information_from_creation(self):
        self.assertEqual(self.survey.start_date, self.truth_start_date)
        self.assertEqual(self.survey.duration, 1.0)
        self.assertEqual(self.survey.idle_delay, 60.0)
        self.assertListEqual(list(self.survey.gen_proposals), GEN_PROPS)
        self.assertIsNone(self.survey.alt_proposal_dir)
        self.assertEqual(self.survey.full_duration, 3650.0)

    def test_alternate_duration(self):
        self.survey.duration = 4500.0
        self.assertEqual(self.survey.full_duration, 4500.0)
