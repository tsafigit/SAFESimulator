import pprint  # Todo TEMP use of pprint - remove
import json
import sys
from Simulator.ProgramIncrement import ProgramIncrement
from Simulator.JIRAUtilities import JIRAUtilities

from Constants import *


def summarize_one_sprint_one_team(team_sprint):
    print("\nTeam %s" % team_sprint.team.name)

    print('Sprint issues')
    print(team_sprint.curr_sprint_all_content_keys)

    print('\nTransition table')
    for day_idx in range(team_sprint.sprint_size):
        print(team_sprint.transition_table.transitions[day_idx])

    stories_in_prog = []
    stories_done = []
    stories_todo = []

    for person in team_sprint.team.team_members:
        stories_done.extend(person.stories_done)
        for story in person.stories_in_progress:
            stories_in_prog.append(story.key)

    for story in team_sprint.curr_sprint_backlog.list_of_issues:
        stories_todo.append(story.key)

    print('\n%d stories done, %d in progress, %d todo' % (len(stories_done), len(stories_in_prog), len(stories_todo)))

    print('\nDone stories:')
    print(stories_done)
    print('In progress stories:')
    print(stories_in_prog)
    print('Todo stories:')
    print(stories_todo)


def summarize_sprint(sprint):
    print('\n\nSUMMARY')
    for team_sprint in sprint.team_sprints:
        #self.summarize_one_sprint_one_team(team_sprint)
        summarize_one_sprint_one_team(team_sprint)

def run_PI(simulation_config_dict):
    if JIRA_INST == 'CLOUD':
        jira_utils = JIRAUtilities('cloud')  # todo: Tsafi 3 Feb 2020: 'cloud' and 'notcloud' preserved for now. To refactor.
    elif JIRA_INST == 'LOCAL':
        jira_utils = JIRAUtilities('notcloud')  # vm version
    else:
        print("*** DEBUG: ERROR - INVALID VALUE FOR JIRA_INST !!!")
        return
    #todo: Tsafi 3 Feb 2020: add an option  without updating Jira todo: TBD depending on test results

    one_pi = ProgramIncrement(simulation_config_dict['train_params'], simulation_config_dict['sprint_params'], jira_utils)

    one_pi.train.initialize_backlogs()

    for day_idx, sprint in enumerate(one_pi.sprints):
        print('\n\n\nSprint %s' % sprint.sprint_name)
        sprint.run_one_sprint()
        #self.summarize_sprint(sprint)
        summarize_sprint(sprint)
        sprint.update_jira_for_sprint()


def load_saved_params():
    file_name = input("Enter file name of a previously saved params file (without the .json suffix): ")
    # todo: verify file exists. Handle exception..
    file_path = DEFAULT_PATH_FOR_SAVED_PARAMS + file_name + ".json"
    with open(file_path) as json_file:
        simulation_config_dict = json.load(json_file)
    # todo: verify file loaded successfully into dict
    print("*** DEBUG: params read from file:")
    pprint.pprint(simulation_config_dict)
    input("*** Press Enter to continue")
    return simulation_config_dict


def get_simulation_params_from_user():

    simulation_config_dict = {}
    print("Enter number of teams between %d and %d (default is %d): "
          % (MIN_NUM_TEAMS, MAX_MUN_TEAMS, DEFAULT_NUM_TEAMS))
    num_teams = int(input() or DEFAULT_NUM_TEAMS)       # ToDo: validate user input

    print("Enter number of sprints between %d and %d (default is %d): "
          % (MIN_NUM_SPRINTS, MAX_NUM_SPRINTS, DEFAULT_NUM_SPRINTS))
    num_sprints = int(input() or DEFAULT_NUM_SPRINTS)     # ToDo: validate user input

    print("Enter sprint size (default is %d): " % DEFAULT_SPRINT_SIZE)   #ToDo: what does the number represents - number of working days, or calendar days?
    # all sprints assumed to be of same size
    sprint_size = int(input() or DEFAULT_SPRINT_SIZE)     # ToDo: validate user input

    # Create sprint_params dict based on user input
    sprint_params = {}
    for i in range(1, num_sprints+1):
        sprint_name = 'Sprint'+str(i)
        sprint_id = 0   # This will be updated on sprint creation in JIRA
        sprint_index = i

        sprint_params[sprint_name] = {
            "sprint_id": sprint_id,
            "sprint_size": sprint_size,
            "sprint_index": sprint_index
         }
    simulation_config_dict['sprint_params'] = sprint_params

    # Create train_params dict based on user input
    # Todo: validate user inputs for all user inputs...
    train_params = {}
    for t in range(1, num_teams+1):
        team_name = 'Dev Team ' + str(t)
        print("\n\nEnter details for team: ", team_name)

        print("Enter num_epics_per_PI (default is %d): " % DEFAULT_NUM_EPICS_PER_PI)
        num_epics_per_PI = int(input() or DEFAULT_NUM_EPICS_PER_PI)

        print("Enter num_stories_per_epic (default is %d): " % DEFAULT_NUM_STORIES_PER_EPIC)
        num_stories_per_epic = int(input() or DEFAULT_NUM_STORIES_PER_EPIC)

        print("Enter story_cycle_time (default is %d): " % DEFAULT_STORY_CYCLE_TIME)
        story_cycle_time = int(input() or DEFAULT_STORY_CYCLE_TIME)

        print("Enter avg_velocity_num_of_stories (default is %d): " % DEFAULT_AVG_VELOCITY_NUM_OF_STORIES)
        avg_velocity_num_of_stories = int(input() or DEFAULT_AVG_VELOCITY_NUM_OF_STORIES)

        print("Enter wip_limit (default is %d): " % DEFAULT_WIP_LIMIT)
        wip_limit = int(input() or DEFAULT_WIP_LIMIT)

        print("Enter prob_for_taking_stories_when_busy (default is %f): " % DEFAULT_PROB_FOR_TAKING_STORIES_WHEN_BUSY)
        prob_for_taking_stories_when_busy = float(input() or DEFAULT_PROB_FOR_TAKING_STORIES_WHEN_BUSY)

        # Tsafi 12 Feb 2020 - get following two new params: prob_for_ShS_delay, and avg_ShS_delay
        print("Enter prob_for_ShS_delay (default is %f): " % DEFAULT_PROB_FOR_SHS_DELAY)
        prob_for_ShS_delay = float(input() or DEFAULT_PROB_FOR_SHS_DELAY)

        print("Enter avg_ShS_delay (default is %d): " % DEFAULT_AVG_SHS_DELAY)
        avg_ShS_delay = float(input() or DEFAULT_AVG_SHS_DELAY)

        print("Enter team_size (default is %d): " % DEFAULT_TEAM_SIZE)
        team_size = int(input() or DEFAULT_TEAM_SIZE)
        #print("*** DEBUG: team size is: ", team_size)
        team_members = []
        for m in range (1, team_size+1):
            team_member_name = team_name + " Member " + str(m)
            team_members.append(team_member_name)
        #print("*** DEBUG: team members: \n", team_members)


        train_params[team_name]={
            "num_epics_per_PI": num_epics_per_PI,
            "num_stories_per_epic": num_stories_per_epic,
            "story_cycle_time": story_cycle_time,
            "avg_velocity_num_of_stories": avg_velocity_num_of_stories,
            "wip_limit": wip_limit,
            "prob_for_taking_stories_when_busy": prob_for_taking_stories_when_busy,
            "prob_for_ShS_delay": prob_for_ShS_delay,  # Tsafi 12 Feb 2020
            "avg_ShS_delay": avg_ShS_delay,  # Tsafi 12 Feb 2020
            "team_members": team_members
        }
        simulation_config_dict['train_params'] = train_params

        #print("*** DEBUG: train_params:")
        #pprint.pprint(simulation_config_dict['train_params'])
    return simulation_config_dict

def save_simulation_params(simulation_config_dict):
    print("Config dict to save:")
    pprint.pprint(simulation_config_dict)
    print("Do you want to save the simulation parameters?")
    r = input("please enter Yes or No: ")
    while (r != "Yes" and r != "No"):
        r = input("Wrong selection! Please enter Yes or No: ")

    if r != "Yes":
        return

    # r == "Yes". User wants to save the params

    file_name = input("Please enter file name: ")
    # todo: validate legal file name
    # todo: check if already exists with same name. Override?
    print("file: " + file_name + " will be saved to this location: " + DEFAULT_PATH_FOR_SAVED_PARAMS + " in .json format")
    j = json.dumps(simulation_config_dict)
    file_path = DEFAULT_PATH_FOR_SAVED_PARAMS + file_name + ".json"  # todo: if file name already ends with ".json" then no need to add...
    with open(file_path, 'w') as outfile:
        json.dump(simulation_config_dict, outfile)
    # todo: verify file saved successfully


print("*** DEBUG: SIMULATION STARTING...\n")

simulation_config_dict = {}
print("Simulation params can be either loaded from a previously saved file or entered manually.")
print("Load params from a previously saved file?")
r = input("Please enter Yes or No: ")
while (r != "Yes" and r != "No"):
    r = input("Wrong selection! Please enter Yes or No: ")

if r == "Yes":
    simulation_config_dict = load_saved_params()
    print("*** DEBUG: after loading saved file\n")
else:
    simulation_config_dict = get_simulation_params_from_user()
    print("*** DEBUG: after getting params from user\n")
    print("*** \nSimulation will run with following params:")
    pprint.pprint(simulation_config_dict)
    input("*** Press Enter to continue")
    save_simulation_params(simulation_config_dict)
    print("*** DEBUG: after save user params. simulation_config_dict:...\n")
    input("*** Press Enter to continue")

run_PI(simulation_config_dict)  # todo: uncomment (temporarily commented out)

print("*** DEBUG: SIMULATION ENDED ***")
