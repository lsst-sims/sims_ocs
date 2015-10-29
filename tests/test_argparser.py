import unittest

from lsst.sims.ocs.setup.parser import create_parser

class ArgParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_parser_creation(self):
        self.assertIsNotNone(self.parser)

    def test_parser_help(self):
        self.assertIsNotNone(self.parser.format_help())

    def test_behavior_with_no_args(self):
        args = self.parser.parse_args([])
        self.assertEqual(args.frac_duration, -1)
        self.assertEqual(args.session_id, "1000")
        self.assertEqual(args.verbose, 0)
        self.assertEqual(args.debug, 0)
        self.assertFalse(args.no_scheduler)
        self.assertIsNone(args.config)
        self.assertFalse(args.save_config)

    def test_fractional_duration_flag(self):
        args = self.parser.parse_args(["--frac-duration", "0.0027397260273972603"])
        self.assertEquals(args.frac_duration, 1.0 / 365.0)

    def test_verbose_flag_count(self):
        args = self.parser.parse_args(["-v", "-v", "-v"])
        self.assertEqual(args.verbose, 3)

    def test_debug_flag_count(self):
        args = self.parser.parse_args(["-d", "-d"])
        self.assertEqual(args.debug, 2)

    def test_no_sched_flag(self):
        args = self.parser.parse_args(["--no-sched"])
        self.assertTrue(args.no_scheduler)

    def test_config_as_file_list(self):
        args = self.parser.parse_args(["--config", "conf1.py", "conf2.py", "conf3.py"])
        self.assertEqual(len(args.config), 3)

    def test_session_id(self):
        args = self.parser.parse_args(["-s", "1100"])
        self.assertEqual(args.session_id, "1100")

    def test_config_files_with_other_option(self):
        args = self.parser.parse_args(["--config", "conf1.py", "conf2.py", "-d"])
        self.assertEqual(len(args.config), 2)

    def test_save_config_flag(self):
        args = self.parser.parse_args(["--save-config"])
        self.assertTrue(args.save_config)
