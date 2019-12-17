from Simulator.JIRAUtilities import JIRAUtilities
from Simulator.Person import Person
from Simulator.BacklogGenerator import BacklogGenerator


class Team:
    def __init__(self, name, params, jira_utils):
        self.name = name
        self.num_epics_per_PI = params["num_epics_per_PI"]
        self.num_stories_per_epic = params["num_stories_per_epic"]
        self.story_cycle_time = params["story_cycle_time"]
        self.avg_velocity_num_of_stories = params["avg_velocity_num_of_stories"]
        self.wip_limit = params["wip_limit"]
        self.prob_for_taking_stories_when_busy = params["prob_for_taking_stories_when_busy"]


        self.team_members = []
        for person_name in params["team_members"]:
            person = Person(person_name, self)
            self.team_members.append(person)

        # The team is the owner of the backlogs
        self.epic_backlog = None
        self.user_story_backlog = None

        self.jira_utils = jira_utils

    def initialize_backlog(self):
        backlog_generator = BacklogGenerator(self.name) #prefix for issue names
        backlog_generator.generate_hierarchy(self.num_epics_per_PI, self.num_stories_per_epic)

        self.epic_backlog = backlog_generator.epic_backlog
        self.user_story_backlog = backlog_generator.user_story_backlog

        self.jira_utils.create_list_of_epics(self.epic_backlog.list_of_issues, self)
        self.jira_utils.create_list_of_user_stories(self.user_story_backlog.list_of_issues, self)

    def reset_done(self):
        for p in self.team_members:
            p.reset_done()
