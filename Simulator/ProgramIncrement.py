from Simulator.Sprint import Sprint
from Simulator.Train import Train


class ProgramIncrement:

    def __init__(self, train_params, sprint_params, jira_utils):
        self.train = Train(train_params, jira_utils)

        self.sprints = []

        for sprint_name in sprint_params:
            sprint = Sprint(sprint_name, sprint_params[sprint_name], self.train, jira_utils)
            self.sprints.append(sprint)

    def run(self):
        self.train.initialize_backlogs()

        for sprint in self.sprints:
            print("Sprint %s" % sprint.sprint_name)
            sprint.run_one_sprint()

        self.update_jira()
