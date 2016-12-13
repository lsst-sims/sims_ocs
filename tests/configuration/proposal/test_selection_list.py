import unittest

from lsst.sims.ocs.configuration.proposal import SelectionList

class SelectionListTest(unittest.TestCase):

    def test_basic_information_after_creation(self):
        sl = SelectionList()
        self.assertListEqual(list(sl.indexes), [])

    def test_list_appending(self):
        sl = SelectionList()
        sl.indexes.append(1)
        sl.indexes.append(3)
        self.assertListEqual(list(sl.indexes), [1, 3])

    def test_list_assignment(self):
        truth_list = [3, 5, 8]
        sl = SelectionList()
        sl.indexes = truth_list
        self.assertListEqual(list(sl.indexes), truth_list)
