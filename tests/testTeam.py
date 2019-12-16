import unittest
from unittest.mock import Mock
from Simulator.Team import Team


class TestTeam(unittest.TestCase):
    _team_params = {
        "num_epics_per_PI" : 3,
        "num_stories_per_epic" : 5,
        "user_stories_board_id": 2,
        "story_cycle_time" : 3,
        "avg_velocity_num_of_stories" : 20,
        "wip_limit": 3,
        "prob_for_taking_stories_when_busy": 0.5,
        "team_members" : ["PersonA", "PersonB", "PersonC"]
    }

    def setUp(self) -> None:
        self.jira_utils = Mock()

        self.team = Team("Dev Team 1", self._team_params, self.jira_utils)

    def test_backlog_params(self):
        self.assertEqual(self.team.num_epics_per_PI, self._team_params["num_epics_per_PI"])
        self.assertEqual(self.team.num_stories_per_epic, self._team_params["num_stories_per_epic"])

    def test_board_params(self):
        self.assertEqual(self.team.user_stories_board_id, self._team_params["user_stories_board_id"])

    def test_cycle_time(self):
        self.assertEqual(self.team.story_cycle_time, self._team_params["story_cycle_time"])
        self.assertEqual(self.team.avg_velocity_num_of_stories, self._team_params["avg_velocity_num_of_stories"])

    def test_team_members(self):
        for idx, person_name in enumerate(self._team_params["team_members"]):
            self.assertEqual(self.team.team_members[idx].name, person_name)

    def test_empty_members_list(self):
        self._team_params["team_members"] = []
        self.team = Team("Dev Team 1", self._team_params, self.jira_utils)
        self.assertEqual(len(self.team.team_members), 0)

if __name__ == '__main__':
    unittest.main()
