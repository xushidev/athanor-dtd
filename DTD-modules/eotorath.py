#################
# Loading cvars #
#################

athanor_dtd = cvar_loader()

################
# Time checker #
################

try:
    before_exhaustion_streak, exhaustion_streak, athanor_dtd = time_checker(athanor_dtd)
except:
    return 'echo You are doing 2 dtds in the same day, please try tomorrow'

###################
# Arguments check #
###################

def_skill1 = athanor_dtd["default_skill1"]
def_skill2 = athanor_dtd["default_skill2"]

a = LIB.numargparse(&ARGS&)
args1 = '&2&'.lower()
args2 = '&3&'.lower()
no_args1 = '&' + '2' + '&'
no_args2 = '&' + '3' + '&'

if (args1 == no_args1 or args2 == no_args2) and (def_skill1 == "" or def_skill2 == ""):
    return 'echo Error: No input given'

if def_skill1 != "" and def_skill2 != "":
    args1 = def_skill1
    args2 = def_skill2

#######################################
# Declaring Allowed Skill/Tools Lists #
#######################################

allowed_tools = [
    "carpenterstools",
    "masonstools",
    "glassblowerstools",
    "weaverstools",
    "cooksutensils",
    "herbalismkit"
]

allowed_skills = [
    "persuasion",
    "medicine",
    "animalHandling",
    "nature",
    "arcana",
    "athletics"
]

################
# input checks #
################

# Search for the skill that matches a valid skill, else it is 'default'
skill1 = ([x for x,y in ch.skills if args1.lower().replace(' ','') in x.lower()]+['default'])[0]

# Search for the tool that matches, else it raises a dict key error
try:
    skill2 = TOOL.matching_tools(args2)[0]
except:
    return 'echo Error: Tool given is not a tool'

if skill1 == 'default':
    return 'echo Error: skill given is not a skill'

if skill1 not in allowed_skills:
    return f'''echo Error: skill given is not an accepted skill
            skill given: {skill2}
            valid skills: {', '.join(allowed_skills)}'''

if skill2 not in allowed_tools:
    return f'''echo Error: tool given is not an accepted tool
            tool given: {skill2}
            valid tools: {', '.join(allowed_tools)}'''

ch.set_cvar("athanor_dtd", dump_json(athanor_dtd))

######################
# Arguments for roll #
######################

# Get possible advantage from the arguments
a.set_context(1)
bonus1 = a.get("b", 0)
adv1 = a.adv()
a.set_context(2)
bonus2 = a.get("b", 0)
adv2 = a.adv()

# Get possible rerolls from arguments (halflings)
reroll_number = ch.csettings.get("reroll", None)

# Gets possible minimum checks from reliable talent or argument
minimum_check1 = a.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[skill1].prof>=1 else None)

########################
# Exhaustion penalties #
########################

exh_msg, adv1, adv2 = exhaustion_penalties(exhaustion_streak, adv1, adv2)

###############
# Final Rolls #
###############

tool_roll_str = TOOL.tool_check_dice_str(skill2, base_adv=ADV_TABLE[adv1])

if bonus1 == 0:
    SkillRoll1 = vroll(ch.skills[skill1].d20(ADV_TABLE[adv1], reroll_number, minimum_check1))
else:
    bonuses = ""
    for bonus in bonus1:
        bonuses += "+" + bonus
    SkillRoll1 = vroll(f"{ch.skills[skill1].d20(ADV_TABLE[adv1], reroll_number, minimum_check1)} {bonuses}")

if bonus2 == 0:
    SkillRoll2 = vroll(tool_roll_str)
else:
    bonuses = ""
    for bonus in bonus2:
        bonuses += "+" + bonus
    SkillRoll2 = vroll(f"{tool_roll_str} {bonuses}")

# Fixes animal handling for display
if skill1 == "animalHandling":
    skill1 = "Animal Handling"
else:
    skill1 = skill1.capitalize()

################
# Final Result #
################

return f'''embed
            -title "Downtime Activity: Job"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {TIER})

**{skill1}:** {SkillRoll1}
**{TOOL_LIST[TOOL.matching_tools(args2)[0]]['name']}:** {SkillRoll2}
"""
            -thumb "{ch.image}"
            -footer "!dtd job [skill1] [skill2] | Athanor | !dtd help"
        '''