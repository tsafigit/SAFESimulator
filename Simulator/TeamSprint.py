import random
from Simulator.TransitionTable import TransitionTable
from Simulator.Backlog import Backlog


class TeamSprint:
    _velocity_max_change_percent = 10
    _user_story_max_change_percent = 20

    def __init__(self, sprint_name, sprint_params, team):
        self.sprint_name = sprint_name
        self.sprint_id = sprint_params["sprint_id"]
        self.sprint_size = sprint_params["sprint_size"]
        self.team = team
        self.jira_utils = team.jira_utils

        # Contains UserStories
        self.curr_sprint_backlog = []
        self.curr_sprint_all_content_keys = []
        self.transition_table = None


    def _value_with_random_deviation(self, value, max_change_percent):
        current_change = random.randrange(max_change_percent)
        pos_or_neg = random.randrange(2)

        if pos_or_neg:
            change = current_change
        else:
            change = -current_change

        value = value * (1 + change / 100)
        return round(value)

    def _find_last_sprint_leftovers(self):
        list_of_leftover_keys = []

        for person in self.team.team_members:
            for story in person.stories_in_progress:
                list_of_leftover_keys.append(story.key)

        print('Leftovers from previous sprint')
        print(list_of_leftover_keys)
        return list_of_leftover_keys

    def _populate_current_sprint_backlog(self, planned_velocity):
        self.curr_sprint_backlog = Backlog()

        self.curr_sprint_all_content_keys.extend(self._find_last_sprint_leftovers())
        list_of_new_story_keys = []

        # deduct the number of leftover stories
        # (stories that are already in progress from previous sprint
        planned_velocity = planned_velocity - len(self.curr_sprint_all_content_keys)

        print('Adding %d stories from the backlog' % int(planned_velocity))

        for idx in range(planned_velocity):
            story_completion_time = self._value_with_random_deviation(self.team.story_cycle_time,
                                                                      self._user_story_max_change_percent)
            story = self.team.user_story_backlog.pick_top_issue()
            story.set_completion_time(story_completion_time)

            self.curr_sprint_backlog.add_issue(story)
            list_of_new_story_keys.append(story.key)

        print('New stories in the sprint')
        print(list_of_new_story_keys)

        self.curr_sprint_all_content_keys.extend(list_of_new_story_keys)

        print('Entire sprint content')
        print(self.curr_sprint_all_content_keys)

    def set_up_sprint(self):
        print('\nTeam %s' % self.team.name)

        #planned_velocity = self._value_with_random_deviation(self.team.avg_velocity_num_of_stories, self._velocity_max_change_percent)
        planned_velocity = self.team.avg_velocity_num_of_stories

        self._populate_current_sprint_backlog(planned_velocity)

        # For now, velocity is in the number of stories
        self.jira_utils.add_issues_from_backlog_to_sprint(self.team.user_stories_board_id, self.curr_sprint_all_content_keys)

        self.transition_table = TransitionTable(self.sprint_size, self.curr_sprint_all_content_keys)

        self.team.reset_done()

    # Note: this is done for comfort the sake of
    # easily adding new stories to the next sprint
    # This should not result in a transition in the
    # transition table
    def cleanup_sprint(self):
        todo_story_keys = []

        for idx, story in enumerate(self.curr_sprint_backlog.list_of_issues):
            self.team.user_story_backlog.add_issue_at_index(idx, story)
            todo_story_keys.append(story.key)

        print('Team %s: Returning ToDo stories to the backlog' % self.team.name)
        print(todo_story_keys)

    def run_one_day(self, day):
        for p in self.team.team_members:
            p.finish_all_done_stories(day, self.transition_table)

        for p in self.team.team_members:
            p.pick_story_for_today_and_work(day, self.curr_sprint_backlog, self.transition_table)

    def run_one_sprint(self):
        print("Team %s" % self.team.name)
        self.set_up_sprint()

        for day in range(self.sprint_size):
            print('Day %d' % (day + 1))
            self.run_one_day(day + 1)

        self.cleanup_sprint()

    def update_one_day_transitions_in_jira(self, day):
        curr_day = self.transition_table.transitions[day - 1]
        for idx, transition in enumerate(curr_day):
            if transition != 0:
                print("idx %d, len %d" % (int(idx), len(self.curr_sprint_backlog.list_of_issues)))
                self.jira_utils.update_one_issue(self.curr_sprint_backlog.list_of_issues[idx], transition)