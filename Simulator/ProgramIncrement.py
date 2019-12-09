from Simulator.Sprint import Sprint
from Simulator.Train import Train


class ProgramIncrement:

    def __init__(self, train_params, sprint_params):
        self.train = Train(train_params)

        self.sprints = []

        for sprint_name in sprint_params:
            sprint = Sprint(sprint_name, sprint_params[sprint_name], self.train)
            self.sprints.append(sprint)

    def update_jira(self, jira_inst):
        for sprint in self.sprints:
            for day_idx in range(sprint.sprint_size):
                sprint.update_one_day_transitions_in_jira(jira_inst, day_idx + 1)

                # ToDo Update the server time

    def run(self, jira_inst):
        self.train.initialize_from_jira(jira_inst)

        for sprint in self.sprints:
            print("Sprint %s" % sprint.sprint_name)
            sprint.run_one_sprint(jira_inst)

        self.update_jira(jira_inst)
