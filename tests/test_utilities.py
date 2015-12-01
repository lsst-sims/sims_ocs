import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.utilities.file_helpers import expand_path
from lsst.sims.ocs.utilities.session_info import get_hostname, get_user, get_version

class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.user = "demouser"
        self.hostname = "tester"
        self.version = "4.0.9.0"

    @mock.patch("os.getenv")
    def test_get_user(self, mock_getenv):
        mock_getenv.return_value = self.user
        self.assertEquals(get_user(), self.user)

    @mock.patch("os.getenv")
    def test_get_hostname(self, mock_getenv):
        mock_getenv.return_value = self.hostname
        self.assertEquals(get_hostname(), self.hostname)

    @mock.patch("socket.gethostname")
    @mock.patch("os.getenv")
    def test_get_hostname_by_socket_gethostname(self, mock_getenv, mock_gethostname):
        mock_getenv.return_value = None
        mock_gethostname.return_value = self.hostname
        self.assertEquals(get_hostname(), self.hostname)

    @mock.patch("lsst.sims.ocs.utilities.session_info.__version__", "0.9.0")
    def test_get_version(self):
        self.assertEquals(get_version(), self.version)

    def test_expand_path(self):
        with mock.patch.dict("os.environ", {"HOME": "/home/{}".format(self.user), "TEST": "testing"}):
            path = "~/$TEST/output"
            self.assertEqual(expand_path(path), "/home/{}/testing/output".format(self.user))
