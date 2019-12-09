import unittest
from Simulator.Team import Team


class TestTeam(unittest.TestCase):
    _team_params = {
        "epic_board_id" : 1,
        "user_stories_board_id": 2,
        "story_cycle_time" : 3,
        "avg_velocity_num_of_stories" : 20,
        "wip_limit": 3,
        "prob_for_taking_stories_when_busy": 0.5,
        "team_members" : ["PersonA", "PersonB", "PersonC"]
    }

    def setUp(self) -> None:
        self.team = Team("Team1", self._team_params)

    def test_board_params(self):
        self.assertEqual(self.team.epic_board_id, self._team_params["epic_board_id"])
        self.assertEqual(self.team.user_stories_board_id, self._team_params["user_stories_board_id"])

    def test_cycle_time(self):
        self.assertEqual(self.team.story_cycle_time, self._team_params["story_cycle_time"])
        self.assertEqual(self.team.avg_velocity_num_of_stories, self._team_params["avg_velocity_num_of_stories"])

    def test_team_members(self):
        for idx, person_name in enumerate(self._team_params["team_members"]):
            self.assertEqual(self.team.team_members[idx].name, person_name)

    def test_empty_members_list(self):
        self._team_params["team_members"] = []
        self.team = Team("Team1", self._team_params)
        self.assertEqual(len(self.team.team_members), 0)

if __name__ == '__main__':
    unittest.main()
