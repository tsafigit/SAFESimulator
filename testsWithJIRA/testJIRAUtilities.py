import unittest
from datetime import datetime
from datetime import timedelta

from Simulator.JIRAUtilities import JIRAUtilities

class TestJIRAUtilities(unittest.TestCase):
    _jira_inst_type = 'cloud'
    #_jira_inst_type = 'virtual_local'

    _sprint_name = "Sprint A"
    _sprint_size = 7
    _board_id = 106

    def setUp(self) -> None:
        self.jira_utils = JIRAUtilities(self._jira_inst_type)

    def tearDown(self) -> None:
        del self.jira_utils

    def test_create_sprint(self):
        start_date = datetime.now()
        sprint = self.jira_utils.create_sprint(self._board_id, self._sprint_name, start_date, self._sprint_size)

        self.assertIsNotNone(sprint)
        self.assertEqual(sprint.name, self._sprint_name)

        end_date = start_date + timedelta(days=self._sprint_size)

        start_date_str = start_date.strftime("%d/%b/%y %#I:%M %p")
        end_date_str = end_date.strftime("%d/%b/%y %#I:%M %p")

        self.assertEqual(sprint.startDate, start_date_str)
        self.assertEqual(sprint.endDate, end_date_str)


if __name__ == '__main__':
    unittest.main()
