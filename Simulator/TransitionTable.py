class TransitionTable:
    _legal_transitions = ['ToDo', 'Prog', 'Imped', 'Done']

    def __init__(self, sprint_size, user_stories_list):
        num_user_stories = len(user_stories_list)

        self.user_stories_list = user_stories_list
        self.transitions = [[0 for x in range(num_user_stories)] for y in range(sprint_size)]

    def _legal_transition_details(self, day, user_story_key, to_state='ToDo'):
        if not (user_story_key in self.user_stories_list):
            return False
        # len of the first dimension is the sprint size
        elif (day <= 0) or (day > len(self.transitions)):
            return False
        elif not (to_state in self._legal_transitions):
            return None

        return True

    def add_transition(self, day, user_story_key, to_state):
        if not (self._legal_transition_details(day, user_story_key, to_state)):
            return False

        user_story_index = self.user_stories_list.index(user_story_key)
        self.transitions[day - 1][user_story_index] = to_state
        return True

    def get_transition(self, day, user_story_key):
        if not (self._legal_transition_details(day, user_story_key)):
            return None

        return self.transitions[day - 1][self.user_stories_list.index(user_story_key)]
