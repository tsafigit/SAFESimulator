import unittest
import random
from unittest.mock import patch
from unittest.mock import Mock

from Simulator.TeamSprint import TeamSprint
from Simulator.Team import Team
from Simulator.UserStory import UserStory
from Simulator.Backlog import Backlog


class TestTeamSprint(unittest.TestCase):
    _sprint_params = {
        "sprint_id" : 1,
        "sprint_size" : 5
    }

    _team_params = {
        "num_epics_per_PI" : 3,
        "num_stories_per_epic" : 5,
        "user_stories_board_id": 2,
        "story_cycle_time" : 3,
        "avg_velocity_num_of_stories" : 20,
        "wip_limit" : 3,
        "prob_for_taking_stories_when_busy" : 0.5,
        "prob_for_ShS_delay": 0,  # Tsafi 12 Feb 2020
        "avg_ShS_delay": 0,  # Tsafi 12 Feb 2020
        "team_members" : ["PersonA", "PersonB", "PersonC", "PersonD", "PersonE"]
    }

    def generate_user_story(self, index):
        name = 'story_' + str(index+1)
        key = 'key_' + str(index+1)

        user_story = UserStory(name)

        user_story.key = key
        user_story.set_completion_time(self._team_params["story_cycle_time"])

        return user_story

    def set_up_team(self):
        team = Team("Test Team", self._team_params, self.jira_utils)
        team.user_story_backlog = Backlog()

        return team

    def setUp(self) -> None:
        self.jira_utils = Mock()
        self.team = self.set_up_team()

        for i in range(self._team_params["avg_velocity_num_of_stories"]):
             self.team.user_story_backlog.add_issue(self.generate_user_story(i))

        for i in range(self._team_params["avg_velocity_num_of_stories"]):
            self.team.user_story_backlog.add_issue(self.generate_user_story(100 + i))

    def summarize_sprint(self, team_sprint):
        print("Team %s" % team_sprint.team.name)

        print('Sprint issues')
        print(team_sprint.curr_sprint_all_content_keys)

        for day_idx in range(team_sprint.sprint_size):
            print(team_sprint.transition_table.transitions[day_idx])

        stories_in_prog = []
        stories_done = []
        stories_todo = []

        for person in team_sprint.team.team_members:
            stories_done.extend(person.stories_done)
            for story in person.stories_in_progress:
                stories_in_prog.append(story.key)

        for story in team_sprint.curr_sprint_backlog.list_of_issues:
            stories_todo.append(story.key)

        print('%d stories done, %d in progress, %d todo' % (len(stories_done), len(stories_in_prog), len(stories_todo)))

        print("Done stories:")
        print(stories_done)
        print("In progress stories:")
        print(stories_in_prog)
        print("Todo stories:")
        print(stories_todo)

    def test_once(self):
        jira_utils = Mock()

        current_sprint = TeamSprint("Test Sprint", self._sprint_params, self.team)
        current_sprint.run_one_sprint()

        self.summarize_sprint(current_sprint)

    def test_setup_second_sprint(self):
        jira_inst = Mock()

        current_sprint = TeamSprint("Test Sprint1", self._sprint_params, self.team)
        current_sprint.run_one_sprint()

        self.summarize_sprint(current_sprint)

        print('\n\nSetting up new sprint')
        new_sprint = TeamSprint("Test Sprint2", self._sprint_params, self.team)
        new_sprint.set_up_sprint()

        self.assertEqual(len(new_sprint.curr_sprint_all_content_keys), self._team_params["avg_velocity_num_of_stories"])

    def test_run_second_sprint(self):
        jira_inst = Mock()

        current_sprint = TeamSprint("Test Sprint1", self._sprint_params, self.team)
        current_sprint.run_one_sprint()

        self.summarize_sprint(current_sprint)

        print('Setting up new sprint')
        new_sprint = TeamSprint("Test Sprint2", self._sprint_params, self.team)
        new_sprint.run_one_sprint()

        self.summarize_sprint(new_sprint)

if __name__ == '__main__':
    unittest.main()
