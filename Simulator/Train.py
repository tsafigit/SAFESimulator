from Simulator.Team import Team


class Train:
    def __init__(self, train_params, jira_utils):
        self.teams = []
        for team_name in train_params:
            team = Team(team_name, train_params[team_name], jira_utils)

            self.teams.append(team)

    def initialize_backlogs(self):
        for team in self.teams:
            team.initialize_backlog()

    def reset_teams(self):
        self.teams.clear()
