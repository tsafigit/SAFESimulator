import os
from datetime import timedelta
from jira import JIRA

# 10124 Story Points

class JIRAUtilities:
    # Translate state changes to JIRA transition values
    transition_ids = {'ToDo': '11', 'Prog': '21', 'Imped': '41', 'Done': '31'}

    user_story_dict_cloud = {
        'project': 'SP',
        #'project': 'TTP',  # Tsafi, 15 Jan 2020
        'issuetype': 'Story',
        'summary': "Story 302",
        'customfield_10322' : [{'value': 'Dev Team 1'}] # Team field ********cloud
    }

    user_story_dict_vm = {
        #'project': 'SP',
        'project': 'TTP', #Tsafi 14 Jan 2020 - temp change to work with TTP project already exists on local Jira
        'issuetype': 'Story',
        'summary': "Story 302",
        #'customfield_10201': [{'value': 'Dev Team 1'}]  # Team field vm
        'customfield_10200': [{'value': 'Dev Team 1'}]  # Tsafi 21 Jan 2020
    }

    # 10120 is the 'Epic Name' and it's a must have
    epic_dict_cloud = {
        'project': 'SP',
        #'project': 'TTP',  # Tsafi, 15 Jan 2020
        #'issuetype': 'Epic',
        'issuetype': {'name': 'Epic'},   # Tsafi 15 Jan 2020
        'summary': "Epic 1",
        'customfield_10120': "Epic 1", # Epic name is the same as Epic summary ********cloud
        'customfield_10322':  [{'value': 'Dev Team 1'}] # Team field ********cloud
    }

    epic_dict_vm = {
        #'project': 'SP',
        'project': 'TTP',  # Tsafi 14 Jan 2020 - temp change to work with TTP project already exists on local Jira
        'issuetype': 'Epic',
        'summary': "Epic 1",
        'customfield_10103': "Epic 1",  # Epic name is the same as Epic summary vm
        #'customfield_10102': "Epic 1",  # Tsafi 14 Jan 2020
        'customfield_10200': [{'value': 'Dev Team 1'}]  # Tsafi 21 Jan 2020 - Team field vm
    }

    def __init__(self, instance_type):
        self.instance_type = instance_type

        if instance_type == 'cloud':
            # Using Nela's Jira cloud account
            #self.jira_inst = JIRA(basic_auth=('nela.g@dr-agile.com', 'FiJBeI3H81sceRofBcY4E84E'),
            #                      options={'server': 'https://dr-agile.atlassian.net'})
            # Using Tsafi's Jira cloud account
            self.jira_inst = JIRA(basic_auth=('tsafrir.m@dr-agile.com', 'tDshA7M9zEhMkaiC13RA146E'),
                                  options={'server': 'https://dr-agile.atlassian.net'})
        else:
            # Using Nela's Jira local VM
            #self.jira_inst = JIRA(basic_auth=('nela.g', 'q1w2e3r4'), options={'server': 'http://192.168.56.101:8080'})
            # Using Tsafi's Jira local VM
            #self.jira_inst = JIRA(basic_auth=('tsafrir.m', 'Sim1965'), options={'server': 'http://192.168.43.55:8080'})
            #self.jira_inst = JIRA(basic_auth=('tsafrir.m', 'Sim1965'), options={'server': 'http://192.168.43.41:8080'})
            self.jira_inst = JIRA(basic_auth=('tsafrir.m', 'Sim1965'), options={'server': 'http://10.0.0.61:8080'})


    def __del__(self):
        del self.jira_inst

    # Creation
    def create_epic(self, name, team):
        if self.instance_type == 'cloud':
            dict = self.epic_dict_cloud
            dict['customfield_10120'] = name   # ********cloud
            dict['customfield_10322'] = [{'value': team.name}] # ********cloud
        else:
            dict = self.epic_dict_vm
            dict['customfield_10103'] = name  # tsafi 21 Jan 2020
            #dict['customfield_10102'] = name # Tsafi 14 Jan 2020
            #dict['customfield_10201'] = {'value': team.name}
            dict['customfield_10200'] = {'value': team.name} # Tsafi 21 Jan 2020

        dict['summary'] = name

        epic = self.jira_inst.create_issue(fields=dict)
        return epic

    def create_user_story_with_epic(self, user_story_name, team, epic_key=None):
        if self.instance_type == 'cloud':
            dict = self.user_story_dict_cloud
            dict['customfield_10322'] = [{'value': team.name}] # ********cloud
        else:
            dict = self.user_story_dict_vm
            #dict['customfield_10201'] = {'value': team.name}
            dict['customfield_10200'] = {'value': team.name} # Tsafi 21 Jan 2020

        dict['summary'] = user_story_name

        user_story = self.jira_inst.create_issue(fields=dict)

        if epic_key:
            self.jira_inst.add_issues_to_epic(epic_key, [user_story.key])

        # Note the performance impact, this is another fetch after
        # adding a story to epic
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

    def advance_time_by_one_day(self):
        if self.instance_type != 'cloud':
            #Tsafi 20 Jan 2020, change path for Tsafi's local VM
            #path = "C:\\Windows\\WinSxS\\amd64_openssh-client-components-onecore_31bf3856ad364e35_10.0.17763.1_none_f0c3262e74c7e35c\\ssh.exe nelkag@192.168.56.101 \"cd /home/nelkag/Simulator/misc; python /home/nelkag/Simulator/misc/advanceoneday.py\""
            #path = "C:\\Windows\\System32\\OpenSSH\\ssh.exe tsafi@192.168.43.41 \"cd /home/tsafi/SAFESimulator; python3 ./advanceoneday.py\""
            #path = "C:\\Windows\\System32\\OpenSSH\\ssh.exe tsafi@10.0.0.61 python3 /home/tsafi/SAFESimulator/advanceoneday.py"
            #path = "C:\\Windows\\System32\\OpenSSH\\ssh.exe tsafi@10.0.0.61 date"
            path = "C:\\Windows\\Sysnative\\OpenSSH\\ssh.exe tsafi@10.0.0.61 python3 ./SAFESimulator/advanceoneday.py"
            print(path)
            os.system(path)