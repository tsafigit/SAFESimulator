from Simulator.JIRAUtilities import JIRAUtilities
from Simulator.Epic import Epic
from Simulator.UserStory import UserStory
from Simulator.Person import Person
from Simulator.Backlog import Backlog


class Team:
    def __init__(self, name, params):
        self.name = name
        self.epic_board_id = params["epic_board_id"]
        self.user_stories_board_id = params["user_stories_board_id"]
        self.story_cycle_time = params["story_cycle_time"]
        self.avg_velocity_num_of_stories = params["avg_velocity_num_of_stories"]
        self.wip_limit = params["wip_limit"]
        self.prob_for_taking_stories_when_busy = params["prob_for_taking_stories_when_busy"]

        self.team_members = []
        for person_name in params["team_members"]:
            person = Person(person_name, self)
            self.team_members.append(person)

        # The team is the owner of the backlogs
        self.epic_backlog = Backlog()
        self.user_story_backlog = Backlog()

        self.jira_utils = JIRAUtilities()

    def _init_epic_backlog(self, jira_inst):
        list_of_epics = self.jira_utils.read_epics_backlog(jira_inst, self.epic_board_id)
        for e in list_of_epics:
            epic = Epic(e)
            self.epic_backlog.add_issue(epic)

    def _init_user_stories_backlog(self, jira_inst):
        list_of_user_stories = self.jira_utils.read_stories_backlog(jira_inst, self.user_stories_board_id)
        for u in list_of_user_stories:
            story = UserStory(u, self.story_cycle_time)
            self.user_story_backlog.add_issue(story)

    def initialize_from_jira(self, jira_inst):
        self._init_epic_backlog(jira_inst)
        self._init_user_stories_backlog(jira_inst)

    def reset_done(self):
        for p in self.team_members:
            p.reset_done()
