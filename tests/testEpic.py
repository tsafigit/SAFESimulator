import unittest
from unittest.mock import Mock
from Simulator.Epic import Epic

class TestEpic(unittest.TestCase):

    _name = 'e1'
    _num_of_stories = 5

    def setUp(self) -> None:
        self.epic = Epic(self._name)

        self.list_of_stories = []
        for i in range(self._num_of_stories):
            story = Mock()
            story.status = 'Prog'
            self.list_of_stories.append(story)

    def test_epic_creation(self):
        self.assertEqual(self.epic.name, self._name)
        self.assertEqual(self.epic.key, None)
        self.assertEqual(self.epic.status, 'ToDo')
        self.assertEqual(len(self.epic.list_of_stories), 0)

    def test_add_story(self):
        story = Mock()
        self.epic.add_story(story)

        self.assertEqual(len(self.epic.list_of_stories), 1)

    def test_add_list_of_stories(self):
        self.epic.add_list_of_stories(self.list_of_stories)

        self.assertEqual(len(self.epic.list_of_stories), 5)

    def test_count_done_on_creation(self):
        self.assertEqual(self.epic.count_done_stories(), 0)

    def test_count_done_some_in_prog(self):
        self.list_of_stories[3].status = 'Done'
        self.epic.add_list_of_stories(self.list_of_stories)
        self.assertEqual(self.epic.count_done_stories(), 1)

    def test_not_done_on_creation(self):
        self.assertEqual(self.epic.check_if_became_done(), False)

    def test_not_done_when_stories_are_not_done(self):
        self.epic.add_list_of_stories(self.list_of_stories)
        self.assertEqual(self.epic.check_if_became_done(), False)

    def test_done_when_stories_are_done(self):
        for i in range(self._num_of_stories):
            self.list_of_stories[i].status = 'Done'

        self.epic.add_list_of_stories(self.list_of_stories)

        self.assertEqual(self.epic.check_if_became_done(), True)

    def test_done_twice_when_stories_are_done(self):
        for i in range(self._num_of_stories):
            self.list_of_stories[i].status = 'Done'

        self.epic.add_list_of_stories(self.list_of_stories)

        self.assertEqual(self.epic.check_if_became_done(), True)
        self.assertEqual(self.epic.check_if_became_done(), False)

    def test_not_became_in_prog_on_creation(self):
        self.assertEqual(self.epic.check_if_became_in_progress(), False)

    def test_became_in_prog(self):
        self.epic.add_list_of_stories(self.list_of_stories)

        self.assertEqual(self.epic.check_if_became_in_progress(), True)
        self.assertEqual(self.epic.check_if_became_in_progress(), False)

    def test_status_change_values(self):
        self.epic.add_list_of_stories(self.list_of_stories)
        self.assertEqual(self.epic.check_if_status_changed(), True)
        self.assertEqual(self.epic.status, 'Prog')

        for i in range(self._num_of_stories):
            self.list_of_stories[i].status = 'Done'

        self.assertEqual(self.epic.check_if_status_changed(), True)
        self.assertEqual(self.epic.status, 'Done')


if __name__ == '__main__':
    unittest.main()
