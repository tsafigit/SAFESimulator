from Simulator.TeamSprint import TeamSprint
from datetime import datetime
from datetime import timedelta
from Constants import JIRA_INST, DEFAULT_JIRA_PARAMS



class Sprint:
    _weekend_size = 2
    #_board_id = 106 #For now, needs to be a param that comes from the PI
    #_board_id = 1
    _board_id = DEFAULT_JIRA_PARAMS[JIRA_INST]['BOARD_ID']  # Tsafi, 3 Feb 2020

    def __init__(self, sprint_name, sprint_params, train, jira_utils):
        self.sprint_name = sprint_name
        self.sprint_id = sprint_params["sprint_id"]
        self.sprint_size = sprint_params["sprint_size"]
        self.sprint_index = sprint_params["sprint_index"]
        self.train = train
        self.jira_utils = jira_utils

        self.team_sprints = []

        self.create_sprint_in_jira()

        for team in self.train.teams:
            sprint_params['sprint_id'] = self.sprint_id
            team_sprint = TeamSprint(self.sprint_name, sprint_params, team)
            self.team_sprints.append(team_sprint)

    def create_sprint_in_jira(self):
        start_date = datetime.now()
        days_delta = (self.sprint_size + self._weekend_size) * (self.sprint_index - 1)
        start_date = start_date + timedelta(days=days_delta)

        sprint = self.jira_utils.create_sprint(self._board_id, self.sprint_name, start_date, self.sprint_size)
        self.sprint_id = sprint.id

    def run_one_day(self, day):
        for team_sprint in self.team_sprints:
            print("\nDay %d Team %s" % (day, team_sprint.team.name))
            team_sprint.run_one_day(day)

    def run_one_sprint(self):
        print('\nSet up Sprint backlog for each team')
        for team_sprint in self.team_sprints:
            team_sprint.set_up_sprint()

        self.jira_utils.start_sprint(self.sprint_id)

        print('\nStarting the work')
        for day_index in range(self.sprint_size):
            print ("\nDay %d" % int(day_index + 1))
            self.run_one_day(day_index + 1)

        print('\nCleanup up Sprint for each team, return items to the backlog')
        for team_sprint in self.team_sprints:
           team_sprint.cleanup_sprint()

    def update_jira_for_sprint(self):
        print('\nUpdating JIRA')
        for day_index in range(self.sprint_size):
            print ("\nDay %d" % int(day_index + 1))
            self.update_one_day_transitions_in_jira(day_index + 1)

        self.update_epic_transitions_for_sprint()

        self.jira_utils.end_sprint(self.sprint_id)

    def update_one_day_transitions_in_jira(self, day):
        for team_sprint in self.team_sprints:
            team_sprint.update_one_day_transitions_in_jira(day)

        #update time here
        self.jira_utils.advance_time_by_one_day()

    def update_epic_transitions_for_sprint(self):
        for team_sprint in self.team_sprints:
            team_sprint.update_epic_transitions_in_jira()
