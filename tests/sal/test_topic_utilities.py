from builtins import str
import unittest

from lsst.sims.ocs.sal import topic_strdict

from tests.database.topic_helpers import target

class TopicUtilitiesTest(unittest.TestCase):

    def test_topic_string_creation(self):
        output = topic_strdict(target)
        self.assertEqual(list(output.keys())[0], "airmass")
        self.assertEqual(output["target_id"], str(target.target_id))
        self.assertEqual(output["sky_angle"], "{:.3f}".format(target.sky_angle))

    def test_topic_string_creation_different_float_format(self):
        new_float_format = "{:.5f}"
        output = topic_strdict(target, float_format=new_float_format)
        self.assertEqual(output["sky_angle"], new_float_format.format(target.sky_angle))
