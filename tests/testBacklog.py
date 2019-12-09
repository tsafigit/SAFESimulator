import unittest
from unittest.mock import Mock
from Simulator.Backlog import Backlog
from Simulator.UserStory import UserStory

class TestBacklog(unittest.TestCase):
    def setUp(self) -> None:
        self.backlog = Backlog()

    def test_empty_backlog(self):
        self.assertEqual(self.backlog.pick_top_issue(), None)

    def test_add_to_list_of_stories(self):
        issue = Mock()
        self.backlog.add_issue(issue)
        self.assertEqual(len(self.backlog.list_of_issues), 1)

    def test_pop_from_list_of_stories(self):
        story = UserStory('key1', 3)
        self.backlog.add_issue(story)
        self.assertEqual(self.backlog.pick_top_issue().key, 'key1')
        self.assertEqual(len(self.backlog.list_of_issues), 0)

    def test_pop_top_item_from_list_of_stories(self):
        story1 = UserStory('key1', 3)
        story2 = UserStory('key2', 3)
        self.backlog.add_issue(story1)
        self.backlog.add_issue(story2)

        self.assertEqual(self.backlog.pick_top_issue().key, 'key1')

if __name__ == '__main__':
    unittest.main()
