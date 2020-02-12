class UserStory:

    def __init__(self, name, epic=None):
        self.name = name
        self.epic = epic
        self.key = None
        self.status = 'ToDo'
        self.assignee = ''
        self.time_left = None
        self._completion_time = None
        self._done_in_parallel = False
        self.wait = 0  # Tsafi 12 Feb 2020: initially no wait time added.

    def set_completion_time(self, completion_time):
        self._completion_time = completion_time
        self.time_left = completion_time

    def work_one_day(self):
        """ Tsafi 12 Feb 2020 - adding delay functionality:
            consume the delay time before start consuming (remaining) work time.
            Old code:
            if self.time_left > 0:
            self.time_left -= 1
            New code below
        """
        if self.wait > 0:
            current_wait = self.wait
            self.wait -= 1
            print("\nStory %s is waiting. Not working on it today. Waiting days: %d -> %d" % (self.name, current_wait, self.wait))
        else:
            if self.time_left > 0:
                self.time_left -= 1

    def update_worked_on_in_parallel(self):
        if self._done_in_parallel:
            return

        print("Story %s is now done in parallel, before %d, after %d" % (self.key, int(self.time_left), int(round(self.time_left * 1.3))))
        self.time_left = round(self.time_left * 1.3)
        self._done_in_parallel = True

    def just_became_done(self):
        if (self.time_left == 0) and (self.status != 'Done'):
            return True
        return False

    def check_if_done_and_update(self, day, transition_table):
        if self.just_became_done():
            self.status = 'Done'
            transition_table.add_transition(day, self.key, 'Done')
            return True
        return False

    def update_status(self, day, to_status, transition_table):
        self.status = to_status
        transition_table.add_transition(day, self.key, to_status)

    def add_wait(self, additional_waiting_days):  # Tsafi 12 Feb 2020
        self.wait += additional_waiting_days

