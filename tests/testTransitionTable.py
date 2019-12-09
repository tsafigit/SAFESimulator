import unittest
from Simulator.TransitionTable import TransitionTable

class TestTransitionTable(unittest.TestCase):
    _sprint_size = 14
    _user_stories_list = ['key1', 'key2', 'key3']

    _day = 3
    _user_story = 'key1'
    _transition = 'ToDo'

    def setUp(self) -> None:
        self.transition_table = TransitionTable(self._sprint_size, self._user_stories_list)

    def test_empty_table(self):
        self.assertEqual(len(self.transition_table.transitions), self._sprint_size)
        self.assertEqual(len(self.transition_table.transitions[0]), len(self._user_stories_list))

    def test_add_transition(self):
        self.transition_table.add_transition(self._day, self._user_story, 'ToDo')
        self.assertEqual(self.transition_table.get_transition(self._day, self._user_story), 'ToDo')

    def test_add_transition_story_not_exists(self):
        result = self.transition_table.add_transition(self._day, 'key_extra', self._transition)
        self.assertEqual(result, False)

    def test_add_day_index_invalid_zero(self):
        result = self.transition_table.add_transition(0, self._user_story, self._transition)
        self.assertEqual(result, False)

    def test_add_day_index_invalid_too_big(self):
        result = self.transition_table.add_transition(self._sprint_size + 1, self._user_story, self._transition)
        self.assertEqual(result, False)

    def test_add_illegal_transition(self):
        result = self.transition_table.add_transition(self._day, self._user_story, 'Something')
        self.assertEqual(result, False)

    def test_get_transition_story_not_exists(self):
        result = self.transition_table.get_transition(self._day, 'key_extra')
        self.assertEqual(result, None)

    def test_get_day_index_invalid_zero(self):
        result = self.transition_table.get_transition(0, self._user_story)
        self.assertEqual(result, None)

    def test_get_day_index_invalid_too_big(self):
        result = self.transition_table.get_transition(self._sprint_size + 1, self._user_story)
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()
