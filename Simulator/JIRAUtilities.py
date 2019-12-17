from jira import JIRA
from datetime import timedelta

# 10124 Story Points
# 10322 Team (list of team names)

class JIRAUtilities:
    # Translate state changes to JIRA transition values
    transition_ids = {'ToDo': '11', 'Prog': '21', 'Imped': '41', 'Done': '31'}

    user_story_dict = {
        'project': 'SP',
        'issuetype': 'Story',
        'summary': "Story 302",
        #'customfield_10124' : 1, # For now, everything is 1 story point
        'customfield_10322' : [{'value': 'Dev Team 1'}] # Team field
    }

    # 10120 is the 'Epic Name' and it's a must have
    epic_dict = {
        'project': 'SP',
        'issuetype': 'Epic',
        'summary': "Epic 1",
        'customfield_10120': "Epic 1", # Epic name is the same as Epic summary
        'customfield_10322':  [{'value': 'Dev Team 1'}] # Team field
    }

    def __init__(self, instance_type):
        if instance_type == 'cloud':
            self.jira_inst = JIRA(basic_auth=('nela.g@dr-agile.com', 'FiJBeI3H81sceRofBcY4E84E'),
                                  options={'server': 'https://dr-agile.atlassian.net'})
        else:
            self.jira_inst = JIRA(basic_auth=('nela.g', 'q1w2e3r4'), options={'server': 'http://192.168.56.101:8080'})

    def __del__(self):
        del self.jira_inst

    # Creation
    def create_epic(self, name, team):
        dict = self.epic_dict
        dict['summary'] = name
        dict['customfield_10120'] = name
        dict['customfield_10322'] = [{'value': team.name}]

        epic = self.jira_inst.create_issue(fields=dict)
        return epic

    def create_user_story_with_epic(self, user_story_name, team, epic_key=None):
        dict = self.user_story_dict
        dict['summary'] = user_story_name
        dict['customfield_10322'] = [{'value': team.name}]

        user_story = self.jira_inst.create_issue(fields=dict)

        if epic_key:
            self.jira_inst.add_issues_to_epic(epic_key, [user_story.key])

        user_story = self.jira_inst.issue(user_story.id)
        return user_story

    def create_list_of_epics(self, list_of_epics, team):
        print('\nCreating list of epics for team %s in JIRA' % team.name)
        for epic in list_of_epics:
            jira_epic = self.create_epic(epic.name, team)
            epic.key = jira_epic.key

    def create_list_of_user_stories(self, list_of_user_stories, team):
        print('\nCreating list of user stories for team %s in JIRA' % team.name)
        for user_story in list_of_user_stories:
            jira_user_story = self.create_user_story_with_epic(user_story.name, team, user_story.epic.key)
            user_story.key = jira_user_story.key


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

    def end_sprint(self, sprint_id):
        print("Please end the sprint manually on a global board")
        key = input()

    def add_issues_to_sprint(self, sprint_id, user_stories_keys):
        print("Adding %d issues to Sprint %d" % (len(user_stories_keys), sprint_id))
        self.jira_inst.add_issues_to_sprint(sprint_id, user_stories_keys)

    def update_one_issue(self, issue_key, transition):
        print("Updating issue %s, moving to %s" % (issue_key, transition))
        self.jira_inst.transition_issue(issue_key, self.transition_ids[transition])
