# Jira instance
#JIRA_INST = 'LOCAL'
JIRA_INST = 'CLOUD'

# Teams
MIN_NUM_TEAMS = 1
MAX_MUN_TEAMS = 10
DEFAULT_NUM_TEAMS = 1

# Team params (defaults for each team)
DEFAULT_NUM_EPICS_PER_PI = 1
DEFAULT_NUM_STORIES_PER_EPIC = 1
DEFAULT_STORY_CYCLE_TIME = 1
DEFAULT_AVG_VELOCITY_NUM_OF_STORIES = 1
DEFAULT_WIP_LIMIT = 1
DEFAULT_PROB_FOR_TAKING_STORIES_WHEN_BUSY = 0.5
DEFAULT_TEAM_SIZE = 1

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

# Other
DEFAULT_PATH_FOR_SAVED_PARAMS = "..\\saved_params\\"  # path to a folder
