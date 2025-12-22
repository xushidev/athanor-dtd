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
        "projects_list": [

        ]
    }
)
athanor_dtd = load_json(ch.get_cvar("athanor_dtd", default))

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
#   "type": "DC/Clock"
# }
#

# DC: DC uses the normal cumulative DC like with spell research (can be like 300 dc and cumulatively add skill checks)
# Clock: has 5 types of difficulties (d4, d6, d8, d10, d12), given a DC there can be +1 or +2 to the clock

###################
# Arguments check #
###################

def_skill1 = athanor_dtd["default_skill1"]
def_skill2 = athanor_dtd["default_skill2"]

a = argparse(&ARGS&)
args1 = '&1&'.lower()
args2 = '&2&'.lower()
no_args1 = '&' + '1' + '&'
no_args2 = '&' + '2' + '&'

if (args1 == no_args1 or args2 == no_args2) and (def_skill1 == "" or def_skill2 == ""):
    return 'echo Error: No input given'

if def_skill1 != "" and def_skill2 != "":
    args1 = def_skill1
    args2 = def_skill2

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


ch.set_cvar("athanor_dtd", dump_json(athanor_dtd))

</drac2>