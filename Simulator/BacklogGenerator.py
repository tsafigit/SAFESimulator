from Simulator.Epic import Epic
from Simulator.UserStory import UserStory
from Simulator.Backlog import Backlog

class BacklogGenerator:
    def __init__(self, prefix):
        self.prefix = prefix

        self.epic_backlog = Backlog()
        self.user_story_backlog = Backlog()

    def create_epic_name(self, num):
        return str(self.prefix) + "Epic" + str(num)

    def create_user_story_name(self, num, epic):
        return epic.name + "_Story" + str(num)

    # This should be the place where stories are
    # prioritized according to some parameter
    # For a well organized team - order remains according
    # to the Epic priority
    # For a 'real-world' team, some shuffling of the stories
    # is needed
    def prioritize_user_stories(self):
        for epic in self.epic_backlog.list_of_issues:
            for story in epic.list_of_stories:
                self.user_story_backlog.add_issue(story)

    def generate_hierarchy(self, epics_num, user_stories_per_epic):
        for e in range(epics_num):
            curr_epic = Epic(self.create_epic_name(e+1))
            self.epic_backlog.add_issue(curr_epic)

            for s in range(user_stories_per_epic):
                curr_story = UserStory(self.create_user_story_name(s+1, curr_epic), curr_epic)
                curr_epic.add_story(curr_story)

        self.prioritize_user_stories()



