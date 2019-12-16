import unittest
from unittest.mock import Mock
from Simulator.Train import Train


class TestTrain(unittest.TestCase):
    _one_team = {
        "Dev Team 1" : {
            "num_epics_per_PI" : 3,
            "num_stories_per_epic" : 5,
            "user_stories_board_id": 2,
            "story_cycle_time" : 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members" : ["PersonA", "PersonB", "PersonC"]
       }
    }

    _many_teams = {
        "Dev Team 1" : {
            "num_epics_per_PI" : 3,
            "num_stories_per_epic" : 5,
            "user_stories_board_id": 2,
            "story_cycle_time" : 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person1A", "Person1B", "Person1C"]
        },
        "Dev Team 2" : {
            "num_epics_per_PI" : 3,
            "num_stories_per_epic" : 5,
            "user_stories_board_id": 5,
            "story_cycle_time" : 6,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person2A", "Person2B", "Person2C"]
        },
        "Dev Team 3" : {
            "num_epics_per_PI" : 3,
            "num_stories_per_epic" : 5,
            "user_stories_board_id": 8,
            "story_cycle_time" : 9,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person3A", "Person3B", "Person3C"]
        }
    }

    def setUp(self) -> None:
        self.jira_utils = Mock()

    def test_team_names(self):
        train = Train(self._many_teams, self.jira_utils)

        self.assertEqual(len(train.teams), len(self._many_teams))
        for i, t in enumerate(self._many_teams):
            self.assertEqual(train.teams[i].name, t)

    def test_clear(self):
        train = Train(self._many_teams, self.jira_utils)
        train.reset_teams()

        self.assertEqual(len(train.teams), 0)


if __name__ == '__main__':
    unittest.main()
