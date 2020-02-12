import unittest
from unittest.mock import Mock
from Simulator.ProgramIncrement import ProgramIncrement

import sys

class JIRAUtilsStub:
    def create_list_of_epics(self, list_of_epics, team):
        for epic in list_of_epics:
            epic.key = epic.name

    def create_list_of_user_stories(self, list_of_user_stories, team):
        for user_story in list_of_user_stories:
            user_story.key = user_story.name

    def add_issues_to_sprint(self, sprint_id, user_stories_keys):
        return None

    def create_sprint(self, board_id, sprint_name, start_date, sprint_size):
        sprint = Mock()
        sprint.id = 1
        return sprint

    def start_sprint(self, sprint_id):
        return

    def end_sprint(self, sprint_id):
        return


class TestProgramIncrement(unittest.TestCase):
    sprint_params = {
        "Sprint1": {
            "sprint_id": 1,
            "sprint_size": 5,
            "sprint_index" : 1
        },
        "Sprint2": {
            "sprint_id": 2,
            "sprint_size": 5,
            "sprint_index" : 2
        }
    }

    small_train_params = {
        "Dev Team 1": {
            "num_epics_per_PI" : 5,
            "num_stories_per_epic" : 10,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "prob_for_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "avg_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "team_members": ["Person1A", "Person1B", "Person1C"]
        }
    }

    train_params = {
        "Dev Team 1": {
            "num_epics_per_PI" : 5,
            "num_stories_per_epic" : 10,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 15,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "prob_for_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "avg_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "team_members": ["Person1A", "Person1B", "Person1C"]
        },
        "Dev Team 2": {
            "num_epics_per_PI" : 5,
            "num_stories_per_epic" : 10,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "prob_for_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "avg_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "team_members": ["Person2A", "Person2B", "Person2C", "Person2D", "Person2E"]
        },
        "Dev Team 3": {
            "num_epics_per_PI" : 5,
            "num_stories_per_epic" : 10,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 10,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "prob_for_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "avg_ShS_delay": 0,  # Tsafi 12 Feb 2020
            "team_members": ["Person3A", "Person3B", "Person3C"]
        }
    }

    def summarize_one_sprint_one_team(self, team_sprint):
        print("\nTeam %s" % team_sprint.team.name)

        print('Sprint issues')
        print(team_sprint.curr_sprint_all_content_keys)

        print('\nTransition table')
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

        print('\n%d stories done, %d in progress, %d todo' % (len(stories_done), len(stories_in_prog), len(stories_todo)))

        print('\nDone stories:')
        print(stories_done)
        print('In progress stories:')
        print(stories_in_prog)
        print('Todo stories:')
        print(stories_todo)

    def summarize_sprint(self, sprint):
        print('\n\nSUMMARY')
        for team_sprint in sprint.team_sprints:
            self.summarize_one_sprint_one_team(team_sprint)

    def setUp(self) -> None:
        self.stdoutcopy = sys.stdout
        # Tsafi: bug fix: change log location to be relative to current working dir
        # sys.stdout = open('C:\\Users\\503127335\\PycharmProjects\\HelloWorld\\log.txt', 'w')
        sys.stdout = open('..\\log\\log.txt', 'w')


    def tearDown(self) -> None:
        sys.stdout.close()
        sys.stdout = self.stdoutcopy

    def test_PI(self):
        jira_utils_stub = JIRAUtilsStub()

        one_pi = ProgramIncrement(self.train_params, self.sprint_params, jira_utils_stub)

        #one_pi.run(jira_inst)
        one_pi.train.initialize_backlogs()

        for sprint in one_pi.sprints:
            print('\n\n\nSprint %s' % sprint.sprint_name)
            sprint.run_one_sprint()
            self.summarize_sprint(sprint)

        # update jira

if __name__ == '__main__':
    unittest.main()
