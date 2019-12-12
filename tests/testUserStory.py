import unittest
from unittest.mock import Mock

from Simulator.UserStory import UserStory


class TestUserStory(unittest.TestCase):
    _name = 'story1'
    _key = 'SP-1'
    _completion_time = 3

    def setUp(self) -> None:
        self.us = UserStory(self._name)
        self.us.set_completion_time(self._completion_time)
        self.us.key = self._key

        self.transition_table_mock = Mock()

    def work_till_done(self):
        for x in range(self._completion_time):
            self.us.work_one_day()

    def test_user_story_creation(self):
        user_story = UserStory(self._name)
        self.assertEqual(user_story.name, self._name)
        self.assertEqual(user_story.epic, None)
        self.assertEqual(user_story.key, None)
        self.assertEqual(user_story.status, 'ToDo')
        self.assertEqual(user_story.assignee, '')
        self.assertEqual(user_story.time_left, None)
        self.assertEqual(user_story._completion_time, None)
        self.assertEqual(user_story._done_in_parallel, False)

    def test_user_story_creation_whith_epic(self):
        epic = Mock()
        user_story = UserStory(self._name, epic)

        self.assertEqual(user_story.epic, epic)

    def test_does_not_become_done_on_creation(self):
        self.assertFalse(self.us.just_became_done())

    def test_work_one_day(self):
        self.us.work_one_day()
        self.assertEqual(self.us.time_left, self._completion_time - 1)
        self.assertFalse(self.us.just_became_done())

    def test_work_till_done(self):
        self.work_till_done()

        self.assertTrue(self.us.just_became_done())

    def test_work_till_done_ask_twice(self):
        self.work_till_done()

        self.assertTrue(self.us.just_became_done())

        # Simulate transition update
        self.us.status = 'Done'

        # For the second time, just became done is not relevant anymore
        self.assertFalse(self.us.just_became_done())

    def test_work_too_much(self):
        for x in range(self._completion_time + 2):
            self.us.work_one_day()

        self.assertTrue(self.us.just_became_done())

    def test_parallelism_first_time(self):
        self.us.update_worked_on_in_parallel()
        self.assertEqual(self.us.time_left, self._completion_time + 1)

    def test_parallelism_second_time(self):
        self.us.update_worked_on_in_parallel()
        self.us.update_worked_on_in_parallel()
        self.us.update_worked_on_in_parallel()
        self.assertEqual(self.us.time_left, self._completion_time + 1)

    def test_transition_update(self):
        self.us.update_status(1, 'ToDo', self.transition_table_mock)

        self.transition_table_mock.add_transition.assert_called_once_with(1, self._key, 'ToDo')
        self.assertEqual(self.us.status, 'ToDo')

    def test_transition_update_when_done(self):
        self.work_till_done()
        self.us.check_if_done_and_update(1, self.transition_table_mock)

        self.transition_table_mock.add_transition.assert_called_once_with(1, self._key, 'Done')
        self.assertEqual(self.us.status, 'Done')

    def test_completion_time_change(self):
        self.us.set_completion_time(self._completion_time + 2)

        self.assertEqual(self.us.time_left, self._completion_time + 2)
        self.assertEqual(self.us._completion_time, self._completion_time + 2)

if __name__ == '__main__':
    unittest.main()
