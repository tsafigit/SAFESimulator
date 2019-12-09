import unittest
from Simulator.Train import Train


class TestTrain(unittest.TestCase):
    _one_team = {
        "Team1" : {
            "epic_board_id" : 1,
            "user_stories_board_id": 2,
            "story_cycle_time" : 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members" : ["PersonA", "PersonB", "PersonC"]
       }
    }

    _many_teams = {
        "Team1" : {
            "epic_board_id" : 1,
            "user_stories_board_id": 2,
            "story_cycle_time" : 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person1A", "Person1B", "Person1C"]
        },
        "Team2" : {
            "epic_board_id" : 4,
            "user_stories_board_id": 5,
            "story_cycle_time" : 6,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person2A", "Person2B", "Person2C"]
        },
        "Team3" : {
            "epic_board_id" : 7,
            "user_stories_board_id": 8,
            "story_cycle_time" : 9,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person3A", "Person3B", "Person3C"]
        }
    }

    def test_team_names(self):
        train = Train(self._many_teams)

        self.assertEqual(len(train.teams), len(self._many_teams))
        for i, t in enumerate(self._many_teams):
            self.assertEqual(train.teams[i].name, t)

    def test_clear(self):
        train = Train(self._many_teams)
        train.reset_teams()

        self.assertEqual(len(train.teams), 0)


if __name__ == '__main__':
    unittest.main()
