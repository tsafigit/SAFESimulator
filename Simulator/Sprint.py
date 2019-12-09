from Simulator.TeamSprint import TeamSprint


class Sprint:
    def __init__(self, sprint_name, sprint_params, train):
        self.sprint_name = sprint_name
        self.sprint_id = sprint_params["sprint_id"]
        self.sprint_size = sprint_params["sprint_size"]
        self.train = train

        self.team_sprints = []

        for team in self.train.teams:
            team_sprint = TeamSprint(self.sprint_name, sprint_params, team)
            self.team_sprints.append(team_sprint)

    def run_one_day(self, day):
        for team_sprint in self.team_sprints:
            print("\nDay %d Team %s" % (day, team_sprint.team.name))
            team_sprint.run_one_day(day)

    def run_one_sprint(self, jira_inst):
        print('\nSet up Sprint backlog for each team')
        for team_sprint in self.team_sprints:
            team_sprint.set_up_sprint(jira_inst)

        print('\nStarting the work')
        for day_index in range(self.sprint_size):
            print ("\nDay %d" % int(day_index + 1))
            self.run_one_day(day_index + 1)

        print('\nCleanup up Sprint for each team, return items to the backlog')
        for team_sprint in self.team_sprints:
           team_sprint.cleanup_sprint()

    def update_one_day_transitions_in_jira(self, jira_inst, day):
        for team_sprint in self.team_sprints:
            team_sprint.update_one_day_transitions_in_jira(jira_inst, day)
