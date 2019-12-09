import random


class Person:
    def __init__(self, name, team):
        self.stories_in_progress = []
        self.stories_done = []
        self.name = name
        self.team = team

    def _should_add_another_story(self):
        prob_range = self.team.prob_for_taking_stories_when_busy * 100
        prob = random.randrange(100)

        if prob <= prob_range:
            print('Decided to get another story (prob %.2f)' % float(self.team.prob_for_taking_stories_when_busy))
        return prob <= prob_range

    def _add_story_from_backlog(self, day, sprint_backlog, transition_table):
        new_story = sprint_backlog.pick_top_issue()
        if new_story is None:
            print("Could not get a new story from the sprint backlog for %s on day %d" % (self.name, day))
            return

        print('(day %d) Person %s +++ %s, time %d' % (day, self.name, new_story.key, new_story.time_left))
        new_story.update_status(day, 'Prog', transition_table)
        new_story.assignee = self.name

        self.stories_in_progress.append(new_story)

    def _update_all_stories_to_be_parallel(self):
        for s in self.stories_in_progress:
            s.update_worked_on_in_parallel()

    def finish_all_done_stories(self, day, transition_table):
        for s in self.stories_in_progress:
            if s.check_if_done_and_update(day, transition_table):
                print('(day %d) Person %s, %s Done' % (day, self.name, s.key))
                self.stories_done.append(s.key)
                self.stories_in_progress.remove(s)

    def pick_story_for_today_and_work(self, day, sprint_backlog, transition_table):
        # Add new stories to this person, if needed
        if len(self.stories_in_progress) == 0:
            self._add_story_from_backlog(day, sprint_backlog, transition_table)

        elif len(self.stories_in_progress) < self.team.wip_limit:
            if self._should_add_another_story():
                self._add_story_from_backlog(day, sprint_backlog, transition_table)
                self._update_all_stories_to_be_parallel()

        # If there are no stories for this person - do nothing
        if len(self.stories_in_progress) > 0:
            # Choose a story to work on for today
            story_index = random.randrange(len(self.stories_in_progress))
            # print('random returned %d' % story_index)

            story_index = int(story_index)
            story_to_work_on = self.stories_in_progress[story_index]

            # Deduct one day
            before = story_to_work_on.time_left
            story_to_work_on.work_one_day()
            after = story_to_work_on.time_left

            print('(day %d) %s working, story %s: time left %d -> %d' % (
                day, self.name, story_to_work_on.key, before, after))
            return story_index
        else:
            print('(day %d) Person %s, NO WORK' % (day, self.name))
            return -1

    def reset_done(self):
        self.stories_done = []
