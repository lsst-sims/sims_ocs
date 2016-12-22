import unittest

from lsst.sims.ocs.setup.tracking import Tracking

try:
    from unittest import mock
except ImportError:
    import mock

class TrackingTest(unittest.TestCase):

    def setUp(self):
        self.session_id_truth = 1000
        self.session_type_truth = "system"
        self.startup_comment_truth = "This is a test."
        self.user = "demouser"
        self.hostname = "tester"
        self.version = '4.0.9.0'
        self.track = Tracking(self.session_id_truth, self.session_type_truth, self.startup_comment_truth)

    def test_basic_information_after_creation(self):
        self.assertEquals(self.track.session_id, self.session_id_truth)
        self.assertEquals(self.track.tracking_url, self.track.opsim_tracking_url + "/tracking.php")
        self.assertEquals(self.track.update_url, self.track.opsim_tracking_url + "/status.php")
        self.assertEquals(self.track.session_type_codes["system"], 2)
        self.assertEquals(self.track.session_type, self.session_type_truth)
        self.assertEquals(self.track.startup_comment, self.startup_comment_truth)

    @mock.patch("logging.Logger.warning")
    @mock.patch("logging.Logger.debug")
    @mock.patch("lsst.sims.ocs.setup.tracking.get_version")
    @mock.patch("lsst.sims.ocs.setup.tracking.get_hostname")
    @mock.patch("lsst.sims.ocs.setup.tracking.get_user")
    @mock.patch("requests.get")
    def run_tracking_call(self, ok_value, log_calls, mock_get, mock_getuser, mock_gethostname,
                          mock_getversion, mock_logdebug, mock_logwarn):
        mock_response = mock.MagicMock()
        mock_response.ok = ok_value
        mock_get.return_value = mock_response

        mock_getuser.return_value = self.user
        mock_gethostname.return_value = self.hostname
        mock_getversion.return_value = self.version
        test_payload = {'sessionID': self.session_id_truth, 'hostname': self.hostname, 'user': self.user,
                        'startup_comment': self.startup_comment_truth,
                        'code_test': self.track.session_type_codes[self.session_type_truth],
                        'status_id': 1.0, 'run_version': self.version}

        self.track.track_session()
        mock_get.assert_called_once_with(self.track.tracking_url, params=test_payload, timeout=3.0)
        self.assertEqual(mock_logdebug.call_count, log_calls[0])
        self.assertEqual(mock_logwarn.call_count, log_calls[1])

    def test_good_tracking_call(self):
        self.run_tracking_call(True, (1, 0))

    def test_bad_tracking_call(self):
        self.run_tracking_call(False, (0, 1))

    @mock.patch("logging.Logger.warning")
    @mock.patch("logging.Logger.debug")
    @mock.patch("lsst.sims.ocs.setup.tracking.get_hostname")
    @mock.patch("requests.get")
    def run_update_call(self, ok_value, log_calls, mock_get, mock_gethostname, mock_logdebug, mock_logwarn):
        mock_response = mock.MagicMock()
        mock_response.ok = ok_value
        mock_get.return_value = mock_response

        mock_gethostname.return_value = self.hostname

        eng_comment = "I think I'm done."

        test_payload = {'sessionID': self.session_id_truth, 'hostname': self.hostname,
                        'eng_comment': eng_comment}

        self.track.update_session(eng_comment)
        mock_get.assert_called_once_with(self.track.update_url, params=test_payload, timeout=3.0)
        self.assertEqual(mock_logdebug.call_count, log_calls[0])
        self.assertEqual(mock_logwarn.call_count, log_calls[1])

    def test_good_update_call(self):
        self.run_update_call(True, (1, 0))

    def test_bad_update_call(self):
        self.run_update_call(False, (0, 1))

    @mock.patch("requests.get")
    def test_override_values_in_track_session(self, mock_get):
        test_payload = {'sessionID': self.session_id_truth, 'hostname': 'titan', 'user': 'missle',
                        'startup_comment': self.startup_comment_truth,
                        'code_test': self.track.session_type_codes[self.session_type_truth],
                        'status_id': 1.0, 'run_version': '4.1.1'}

        self.track.track_session(hostname='titan', user='missle', version='4.1.1')
        mock_get.assert_called_once_with(self.track.tracking_url, params=test_payload, timeout=3.0)

    @mock.patch("requests.get")
    def test_override_values_in_update_session(self, mock_get):

        eng_comment = "Forgot to update this."

        test_payload = {'sessionID': self.session_id_truth, 'hostname': 'titan',
                        'eng_comment': eng_comment}

        self.track.update_session(eng_comment, hostname='titan')
        mock_get.assert_called_once_with(self.track.update_url, params=test_payload, timeout=3.0)
