class Backlog:

    def __init__(self):
         self.list_of_issues = []

    def add_issue(self, issue):
        self.list_of_issues.append(issue)

    def add_issue_at_index(self, idx, issue):
        self.list_of_issues.insert(idx, issue)

    def pick_top_issue(self):
        if len(self.list_of_issues) == 0:
            return None

        top_issue = self.list_of_issues.pop(0)
        return top_issue
