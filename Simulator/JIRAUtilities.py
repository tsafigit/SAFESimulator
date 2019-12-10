from jira import JIRA
from datetime import timedelta


class JIRAUtilities:
    def __init__(self, instance_type):
        if instance_type == 'cloud':
            self.jira_inst = JIRA(basic_auth=('nela.g@dr-agile.com', 'FiJBeI3H81sceRofBcY4E84E'),
                                  options={'server': 'https://dr-agile.atlassian.net'})
        else:
            self.jira_inst = JIRA(basic_auth=('nela.g', 'q1w2e3r4'), options={'server': 'http://192.168.56.101:8080'})

    def __del__(self):
        del self.jira_inst

    # Creation

    # Create Sprint
    # Best would be to provide a board_id of a board that contains all issues
    def create_sprint(self, board_id, sprint_name, start_date, sprint_size):
        end_date = start_date + timedelta(days=sprint_size)

        start_date_str = start_date.strftime("%d/%b/%y %#I:%M %p")
        end_date_str = end_date.strftime("%d/%b/%y %#I:%M %p")
        print(start_date_str)
        print(end_date_str)

        new_sprint = self.jira_inst.create_sprint(sprint_name, board_id, startDate=start_date_str, endDate=end_date_str)

        print("Created new Sprint: name = %s, id =  %s" % (new_sprint.name, new_sprint.id))
        print("Start date %s, end date %s" % (new_sprint.startDate, new_sprint.endDate))

        return new_sprint

    # Set up Sprints
    def start_sprint(self, sprint_id):
        print("Please start the sprint manually on a global board")
        key = input()

    # Update transitions
    def read_epics_backlog(self, jira_inst, board_id):
        if board_id == 1:
            return ['epic1_1', 'epic1_2', 'epic1_3']
        elif board_id == 4:
            return ['epic2_1', 'epic2_2', 'epic2_3']
        elif board_id == 7:
            return ['epic3_1', 'epic3_2', 'epic3_3']

        return []

    def read_stories_backlog(self, jira_inst, board_id):
        stories_list = []
        team_index = int(board_id / 3) + 1
        for i in range(50):
            story_key = "story" + str(team_index) + "_" + str(i+1)
            stories_list.append(story_key)

        return stories_list

    def add_issues_from_backlog_to_sprint(self, jira_inst, board_id, user_stories_keys):
        return None

    def update_one_issue(self, issue_key, transition):
        return None
