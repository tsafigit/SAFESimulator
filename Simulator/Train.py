from Simulator.Team import Team


class Train:
    def __init__(self, train_params):
        self.teams = []
        for team_name in train_params:
            team = Team(team_name, train_params[team_name])

            self.teams.append(team)

    def initialize_from_jira(self, jira_inst):
        for team in self.teams:
            team.initialize_from_jira(jira_inst)

    def reset_teams(self):
        self.teams.clear()
