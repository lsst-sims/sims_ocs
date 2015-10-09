import unittest

from lsst.sims.ocs.kernel.simulator import Simulator

class SimulatorTest(unittest.TestCase):

    def setUp(self):
        self.sim = Simulator(0.5)

    def test_initial_creation(self):
        self.assertEqual(self.sim.duration, 183.0)
        self.assertEqual(self.sim.time_handler.initial_timestamp, 1590278400.0)

    def test_fraction_overwrite(self):
        self.sim.fractional_duration = 1.0 / 365.0
        self.assertEqual(self.sim.duration, 1.0)
