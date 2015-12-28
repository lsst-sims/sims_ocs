import math
import unittest

from lsst.sims.ocs.configuration.field import Field

from ..database.topic_helpers import field_topic

class FieldTest(unittest.TestCase):

    def setUp(self):
        self.field = Field(1, 0.5, 30.0, -30.0, -45.0, 45.0, 60.0, -60.0)

    def test_initial_creation_from_constructor(self):
        self.assertEqual(self.field.fid, 1)
        self.assertEqual(self.field.fov, 0.5)
        self.assertEqual(self.field.ra, 30.0)
        self.assertEqual(self.field.dec_rads, math.radians(-30.0))
        self.assertEqual(self.field.gl_rads, math.radians(-45.0))
        self.assertEqual(self.field.gb, 45.0)
        self.assertEqual(self.field.el, 60.0)
        self.assertEqual(self.field.eb_rads, math.radians(-60.0))

    def test_initial_creation_from_topic(self):
        ft = Field.from_topic(field_topic)
        self.assertEqual(ft.fid, 1)
        self.assertEqual(ft.fov_rads, math.radians(0.5))
        self.assertEqual(ft.ra_rads, math.radians(30.0))
        self.assertEqual(ft.dec, -30.0)
        self.assertEqual(ft.gl, -45.0)
        self.assertEqual(ft.gb_rads, math.radians(45.0))
        self.assertEqual(ft.el_rads, math.radians(60.0))
        self.assertEqual(ft.eb, -60.0)
