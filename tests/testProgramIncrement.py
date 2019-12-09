import unittest
from unittest.mock import Mock
from Simulator.ProgramIncrement import ProgramIncrement

import sys

class TestProgramIncrement(unittest.TestCase):
    sprint_params = {
        "Sprint1": {
            "sprint_id": 1,
            "sprint_size": 7
        },
        "Sprint2": {
            "sprint_id": 2,
            "sprint_size": 7
        }
    }

    small_train_params = {
        "Team1": {
            "epic_board_id": 1,
            "user_stories_board_id": 2,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person1A", "Person1B", "Person1C"]
        }
    }

    train_params = {
        "Team1": {
            "epic_board_id": 1,
            "user_stories_board_id": 2,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 15,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person1A", "Person1B", "Person1C"]
        },
        "Team2": {
            "epic_board_id": 4,
            "user_stories_board_id": 5,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 20,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
            "team_members": ["Person2A", "Person2B", "Person2C", "Person2D", "Person2E"]
        },
        "Team3": {
            "epic_board_id": 7,
            "user_stories_board_id": 8,
            "story_cycle_time": 3,
            "avg_velocity_num_of_stories": 10,
            "wip_limit": 3,
            "prob_for_taking_stories_when_busy": 0.5,
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
        sys.stdout = open('C:\\Users\\503127335\\PycharmProjects\\HelloWorld\\log.txt', 'w')

    def tearDown(self) -> None:
        sys.stdout.close()
        sys.stdout = self.stdoutcopy

    def test_PI(self):
        one_pi = ProgramIncrement(self.train_params, self.sprint_params)

        jira_inst = Mock()
        #one_pi.run(jira_inst)
        one_pi.train.initialize_from_jira(jira_inst)

        for sprint in one_pi.sprints:
            print('\n\n\nSprint %s' % sprint.sprint_name)
            sprint.run_one_sprint(jira_inst)
            self.summarize_sprint(sprint)

        # update jira

if __name__ == '__main__':
    unittest.main()
