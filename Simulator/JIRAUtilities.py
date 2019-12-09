

class JIRAUtilities:
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