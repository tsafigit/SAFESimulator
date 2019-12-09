import unittest
import random
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import call

from Simulator.UserStory import UserStory
from Simulator.Person import Person
from Simulator.TransitionTable import TransitionTable


class TestPerson(unittest.TestCase):
    _day = 1
    _key = 'key1'
    _completion_time = 3

    def setUp(self) -> None:
        team = Mock()
        team.wip_limit = 3
        team.prob_for_taking_stories_when_busy = 0.5

        self.person = Person("Person 1", team)

        # Access list of 1 stories, then toss 1, then access a list again
        self.randrange_orig = random.randrange
        random.randrange = Mock()
        random.randrange.side_effect = [0, 1, 0]

        self.backlog_mock = Mock()
        self.backlog_mock.pick_top_issue.return_value = UserStory(self._key, self._completion_time)

    def tearDown(self) -> None:
        random.randrange = self.randrange_orig

    def test_new_person(self):
        self.assertEqual(len(self.person.stories_in_progress), 0)
        self.assertEqual(len(self.person.stories_done), 0)

    @patch('Simulator.TransitionTable')
    def test_pick_a_story_when_person_not_busy(self, transition_table_mock):

        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        self.assertEqual(len(self.person.stories_in_progress), 1)

        self.backlog_mock.pick_top_issue.assert_called_once()
        transition_table_mock.add_transition.assert_called_once_with(self._day, self._key, 'Prog')

    @patch('Simulator.TransitionTable')
    def test_pick_a_story_when_person_is_busy(self, transition_table_mock):

        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)
        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        #random is configured to return 1 when deciding if to pick another story
        self.assertEqual(len(self.person.stories_in_progress), 2)
        self.assertEqual(self.backlog_mock.pick_top_issue.call_count, 2)

    @patch('Simulator.TransitionTable')
    def test_dont_pick_a_story_when_person_is_busy(self, transition_table_mock):

        # Access list of 1 stories, then toss 1, then access a list again
        random.randrange.side_effect = [0,99,0]

        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)
        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        self.assertEqual(len(self.person.stories_in_progress), 1)
        self.assertEqual(self.backlog_mock.pick_top_issue.call_count, 1)
        transition_table_mock.add_transition.assert_called_once_with(self._day, self._key, 'Prog')

    @patch('Simulator.TransitionTable')
    def test_parallelism(self, transition_table_mock):
        # Only key1, starts with 3 days, becomes 2 days
        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        # Story key2 is added
        # key1 time_left increases from 2 to 3, then it is worked on, so time_left becomes 2
        # key2 increases from 3 to 4 and stays like that
        self.backlog_mock.pick_top_issue.return_value = UserStory('key2', self._completion_time)
        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        self.assertEqual(self.person.stories_in_progress[0].time_left, self._completion_time - 1)
        self.assertEqual(self.person.stories_in_progress[1].time_left, self._completion_time + 1)

    @patch('Simulator.TransitionTable')
    def test_no_new_story_in_backlog(self, transition_table_mock):

        # No more stories in backlog
        self.backlog_mock.pick_top_issue.return_value = None
        self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        self.assertEqual(len(self.person.stories_in_progress), 0)
        transition_table_mock.add_transition.assert_not_called()


    @patch('Simulator.TransitionTable')
    def test_done_stories(self, transition_table_mock):
        # Always return 0
        random.randrange.side_effect = [0, 99, 0, 99, 0, 99, 0]

        for d in range(self._completion_time):
            self.person.pick_story_for_today_and_work(self._day, self.backlog_mock, transition_table_mock)

        self.person.finish_all_done_stories(self._day, transition_table_mock)

        self.assertEqual(len(self.person.stories_in_progress), 0)

        expected_calls = [call(1, 'key1', 'Prog'), call(1, 'key1', 'Done')]
        self.assertEqual(transition_table_mock.add_transition.call_count, 2)
        self.assertEqual(transition_table_mock.add_transition.call_args_list, expected_calls)

    # Todo - test done stories list
if __name__ == '__main__':
    unittest.main()
