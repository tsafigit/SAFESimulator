import unittest
from Simulator.BacklogGenerator import BacklogGenerator

class TestBacklogGenerator(unittest.TestCase):
    _epics_num = 3
    _stories_num = 5

    def setUp(self) -> None:
        self.backlog_generator = BacklogGenerator('')

    def test_creation(self):
        self.assertEqual(self.backlog_generator.prefix, '')

    def test_generate_hierarchy(self):
        #Tsafi 12 Feb 2020 - added two params with value 0 (test without adding ShS delay
        #self.backlog_generator.generate_hierarchy(self._epics_num, self._stories_num)
        self.backlog_generator.generate_hierarchy(self._epics_num, self._stories_num, 0, 0)

        self.assertEqual(len(self.backlog_generator.epic_backlog.list_of_issues), self._epics_num)
        self.assertEqual(len(self.backlog_generator.user_story_backlog.list_of_issues), self._epics_num*self._stories_num)

    def test_epics(self):
        # Tsafi 12 Feb 2020 - added two params with value 0 (test without adding ShS delay
        #self.backlog_generator.generate_hierarchy(self._epics_num, 1)
        self.backlog_generator.generate_hierarchy(self._epics_num, 1, 0, 0)
        for idx, e in enumerate(self.backlog_generator.epic_backlog.list_of_issues):
            self.assertEqual(e.name, "Epic" + str(idx+1))

    def test_stories(self):
        stories_num = 12

        #Tsafi 12 Feb 2020 - added two params with value 0 (test without adding ShS delay
        #self.backlog_generator.generate_hierarchy(self._epics_num, stories_num)
        self.backlog_generator.generate_hierarchy(self._epics_num, stories_num, 0, 0)
        for epic_idx, e in enumerate(self.backlog_generator.epic_backlog.list_of_issues):
            for story_idx in range(stories_num):
                curr_name = self.backlog_generator.user_story_backlog.list_of_issues[epic_idx*stories_num + story_idx].name
                print(curr_name)
                self.assertEqual(curr_name, "Epic" + str(epic_idx + 1) + "_Story" + str(story_idx+1))
