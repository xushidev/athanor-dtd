<drac2>
#########################
# CONSTANTS definitions #
#########################

ch = character()

TIER = int(level//4.01+1)

TIME = floor(time())

COINPURSE_BEFORE = ch.coinpurse.compact_str()

#################
# Loading cvars #
#################

default = dump_json(
    {
        "last_dtd": "",
        "exhaustion_streak": 0,
        "default_skill1": "",
        "default_skill2": "",
        "projects_list": []
    }
)
athanor_dtd = load_json(ch.get_cvar("athanor_dtd", default))

projects_list = athanor_dtd["projects_list"]

#
# each project in projects_list:
# {
#   "project_name": "Project name",
#   "skill": "skill",
#   "dc": "300",
#   "args": {
#           "b": "1",
#           "adv": "True"
#       },
#   "progress": "0",
#   "description": "any given description of the project",
#   "type": "DC/Clock",
#   "cost": "cost in gp"
# }
#

# DC: DC uses the normal cumulative DC like with spell research (can be like 300 dc and cumulatively add skill checks)
# Clock: has 5 types of difficulties (d4, d6, d8, d10, d12), given a DC there can be +1 or +2 to the clock

###################
# Arguments check #
###################

# arguments:
# !alias "project name" "skill" -dc "amount" -type "dc/clock/1" -desc "optional description" -cost "optional cost in gp"

a = argparse(&ARGS&)
args1 = '&1&'.lower()
args2 = '&2&'.lower()
no_args1 = '&' + '1' + '&'
no_args2 = '&' + '2' + '&'

# loading all the arguments needed
project_dc = a.last("dc", "")
project_type = a.last("type", "")
project_desc = a.last("desc", "")
project_cost = a.last("cost", 0.0)
project_bonus = a.last("b", 0)
project_adv = a.adv(boolwise=True)

if args1 == no_args1:
    return 'echo Error: No project name given'

# we assume progress is 0 to begin with
project_progress = 0

# variable to note if the project is new or not
new_project = True

# if user doesn't give a 2nd argument, it means that he wants it automated
index = -1
if args2 == no_args2:
    
    for list_index, project in enumerate(projects_list):
        args1, project = args1.lower(), project['project_name'].lower()
        common = sum(min(args1.count(c), project['project_name'].count(c)) for c in set(args1))
        if (common / max(len(args1), len(project['project_name']))) > 0.80:
            args1 = project["project_name"]
            index = list_index
    if index == -1:
        return "echo Couldn't find the project in the projects list"
    
    args2 = projects_list[index]['skill']
    project_dc = projects_list[index]['dc']
    project_adv = projects_list[index]['args']['adv']
    project_bonus = projects_list[index]['args']['b']
    project_desc = projects_list[index]['description']
    project_type = projects_list[index]['type']
    project_cost = projects_list[index]['cost']
    project_progress = projects_list[index]['progress']
    new_project = False
else:
    # else it means that this is a new project
    if project_dc == "":
        return "echo Project's DC isn't given"
    
    # we assume if no project type, then it is a one time project
    if project_type == "":
        project_type = "1"

# Pseudo fuzzy search the skill
skill = ([x for x,y in ch.skills if args2.lower().replace(' ','') in x.lower()]+['default'])[0]
if skill == 'default':
    return "echo Skill given isn't a valid skill!"



################
# Time checker #
################

last_dtd = athanor_dtd["last_dtd"]
before_exhaustion_streak = athanor_dtd["exhaustion_streak"]

athanor_dtd["last_dtd"] = TIME

if last_dtd != "":
    if (last_dtd // 86400) == (TIME // 86400):
        return 'echo You are doing 2 dtds in the same day, please try tomorrow'
    if ((last_dtd // 86400) - (TIME // 86400)) >= 2:
        athanor_dtd["exhaustion_streak"] = 0
    else:
        athanor_dtd["exhaustion_streak"] += 1

exhaustion_streak = athanor_dtd["exhaustion_streak"]

####################
# loading the cvar #
####################


# assuming everything goes alright, we append the new project into the cvar
if new_project:
    athanor_dtd['projects_list'].append({
        "project_name": args1,
        "skill": skill,
        "dc": project_dc,
        "args": {
            "b": project_bonus,
            "adv": project_adv
        },
        "progress": project_progress,
        "description": project_desc,
        "type": project_type,
        "cost": project_cost
    })
else:
    # if the project exists, then we override it
    athanor_dtd['projects_list'][index] = {
        "project_name": args1,
        "skill": skill,
        "dc": project_dc,
        "args": {
            "b": project_bonus,
            "adv": project_adv
        },
        "progress": project_progress,
        "description": project_desc,
        "type": project_type,
        "cost": project_cost
    }


ch.set_cvar("athanor_dtd", dump_json(athanor_dtd))

</drac2>