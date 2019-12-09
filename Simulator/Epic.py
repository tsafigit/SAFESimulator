class Epic:
    def __init__(self, key):
        self.key = key
        self.status = 'ToDo'
        self.list_of_stories = []

    def add_story(self, story):
        self.list_of_stories.append(story)

    def add_list_of_stories(self, stories):
        self.list_of_stories.extend(stories)

    def count_done_stories(self):
        count = 0
        for s in self.list_of_stories:
            if s.status == 'Done':
                count += 1

        return count

    def check_if_became_done(self):
        # This is meaningless
        if len(self.list_of_stories) == 0:
            return False

        # This Epic became done earlier
        if self.status == 'Done':
            return False

        if self.count_done_stories() == len(self.list_of_stories):
            self.status = 'Done'
            return True

        return False

    def check_if_became_in_progress(self):
        # This is meaningless
        if len(self.list_of_stories) == 0:
            return False

        if self.status == 'Prog':
            return False

        for s in self.list_of_stories:
            if s.status == 'Prog':
                self.status = 'Prog'
                return True

        return False

    def check_if_status_changed(self):
        if self.check_if_became_done():
            return True

        if self.check_if_became_in_progress():
            return True

        return False
