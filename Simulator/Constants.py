# Jira instance
JIRA_INST = 'LOCAL'
#JIRA_INST = 'CLOUD'

CONTEXT_SWITCH_RATIO = 1.3
# Tsafi, 12 Feb 2020: e.g. 1.3 means that when a story is done in parallel with other stories,
# 30% more time will be required to complete it (due to context switch)

# Teams
MIN_NUM_TEAMS = 1
MAX_MUN_TEAMS = 4  # e.g 3 Dev teams + 1 ShS team
DEFAULT_NUM_TEAMS = 1

# Team params (defaults for each team)
DEFAULT_NUM_EPICS_PER_PI = 1
DEFAULT_NUM_STORIES_PER_EPIC = 1
DEFAULT_STORY_CYCLE_TIME = 1
DEFAULT_AVG_VELOCITY_NUM_OF_STORIES = 1
DEFAULT_WIP_LIMIT = 1
DEFAULT_PROB_FOR_TAKING_STORIES_WHEN_BUSY = 0.5
DEFAULT_TEAM_SIZE = 1
DEFAULT_PROB_FOR_SHS_DELAY = 0  # Tsafi 12 Feb 2020
DEFAULT_AVG_SHS_DELAY = 0  # Tsafi 12 Feb 2020

# Sprint
MIN_NUM_SPRINTS = 1
MAX_NUM_SPRINTS = 5
DEFAULT_NUM_SPRINTS = 1
DEFAULT_SPRINT_SIZE = 5

# Jira
LOCAL_JIRA_IP = '10.0.0.61'
#LOCAL_JIRA_IP = '192.168.43.41'

DEFAULT_JIRA_PARAMS = {
    'LOCAL': {
        'URL': 'http://' + LOCAL_JIRA_IP + ':8080',
        'USER': 'tsafrir.m',
        'PASS': 'Sim1965',
        'PROJECT': 'TTP',
        'BOARD_ID': 1

    },
    'CLOUD': {
        'URL': 'https://dr-agile.atlassian.net',
        'USER': 'tsafrir.m@dr-agile.com',
        'PASS': 'tDshA7M9zEhMkaiC13RA146E',  # Token
        'PROJECT': 'SP',
        'BOARD_ID': 106

    }
}

# Dependencies
"""
SHS_PROBABILITY - when the simulator creates a story s1 for a team,
it will also randomly create (ot not) another story s2 for a ShS team, and make s1 dependent on s2

SHS_TEAM_NAME - holds the name in Jira, of the team that represents a ShS ("ShS Team 1")
"""
SHS_PROBABILITY = 0.5
SHS_TEAM_NAME = "ShS Team 1"

# Other
DEFAULT_PATH_FOR_SAVED_PARAMS = "..\\saved_params\\"  # path to a folder
