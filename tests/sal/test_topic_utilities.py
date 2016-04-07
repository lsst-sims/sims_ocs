import unittest

from lsst.sims.ocs.sal import topic_strdict

from tests.database.topic_helpers import target

class TopicUtilitiesTest(unittest.TestCase):

    def test_topic_string_creation(self):
        output = topic_strdict(target)
        self.assertEqual(output.keys()[0], "angle")
        self.assertEqual(output["targetId"], str(target.targetId))
        self.assertEqual(output["angle"], "{:.3f}".format(target.angle))
        self.assertEqual(output["exposure_times"], str(target.exposure_times))

    def test_topic_string_creation_different_float_format(self):
        new_float_format = "{:.5f}"
        output = topic_strdict(target, float_format=new_float_format)
        self.assertEqual(output["angle"], new_float_format.format(target.angle))
