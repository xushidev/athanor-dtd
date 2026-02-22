############################
# Loading Custom Constants #
############################

VALID_SKILLS1 = ["acrobatics", "athletics", "stealth"]
VALID_SKILLS2 = ["animalHandling", "deception", "intimidation", "investigation", "nature", "perception"]

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

######################
# Skill input checks #
######################

# Search for the skill that matches a valid skill, else it is 'default'
skill1 = ([x for x,y in ch.skills if args1.lower().replace(' ','') in x.lower()]+['default'])[0]
skill2 = ([x for x,y in ch.skills if args2.lower().replace(' ','') in x.lower()]+['default'])[0]

if skill1 == 'default' or skill2 == 'default':
    return 'echo Error: skills given are not skills'

if skill1 not in VALID_SKILLS1:
    return f'''echo Error: skill given is not an accepted skill
            skill given: {skill2}
            valid skills: {', '.join(VALID_SKILLS1)}'''

if skill2 not in VALID_SKILLS2:
    return f'''echo Error: skill given is not an accepted skill
            skill given: {skill2}
            valid skills: {', '.join(VALID_SKILLS2)}'''

athanor_dtd["default_skill1"] = skill1
athanor_dtd["default_skill2"] = skill2

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
minimum_check2 = a.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[skill2].prof>=1 else None)

########################
# Exhaustion penalties #
########################

exh_msg, adv1, adv2 = exhaustion_penalties(exhaustion_streak, adv1, adv2)

#####################
# Final Skill Rolls #
#####################

if bonus1 == 0:
    SkillRoll1 = vroll(ch.skills[skill1].d20(ADV_TABLE[adv1], reroll_number, minimum_check1))
else:
    bonuses = ""
    for bonus in bonus1:
        bonuses += "+" + bonus
    SkillRoll1 = vroll(f"{ch.skills[skill1].d20(ADV_TABLE[adv1], reroll_number, minimum_check1)} {bonuses}")

if bonus2 == 0:
    SkillRoll2 = vroll(ch.skills[skill2].d20(ADV_TABLE[adv2], reroll_number, minimum_check2))
else:
    bonuses = ""
    for bonus in bonus2:
        bonuses += "+" + bonus
    SkillRoll2 = vroll(f"{ch.skills[skill2].d20(ADV_TABLE[adv2], reroll_number, minimum_check2)} {bonuses}")

# Fixes animal handling for display
if skill2 == "animalHandling":
    skill2 = "Animal Handling"
else:
    skill2 = skill2.capitalize()

##########################
# Gold & Penalties Rolls #
##########################

r1_gold = 0
r2_gold = 0

# Checks if failed or succeeded
if SkillRoll1.total < DC_INDEX[0]:
    # failure
    r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    r1_gold -= (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
elif SkillRoll1.total < DC_INDEX[1]:
    # success
    r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
else:
    # critical success
    r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)

if SkillRoll2.total < DC_INDEX[0]:
    # failure
    r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    r2_gold -= (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
elif SkillRoll2.total < DC_INDEX[1]:
    # success
    r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
else:
    # critical success
    r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)

###############################
# Finally modifying coinpurse #
###############################

# if either rolls are lower than 0, then round them up to 0
if r1_gold < 0:
    r1_gold = 0

if r2_gold < 0:
    r2_gold = 0

# Summing up total gold earned
total_gold = r1_gold + r2_gold

# If the total gold is less than 0, make it 0
if total_gold < 0:
    total_gold = 0

# Parsing the gold
parsed_coins = parse_coins(f"{total_gold}", include_total=False)

# Modifying the coinpurse
changes = ch.coinpurse.modify_coins(**parsed_coins)

COINPURSE_AFTER = ch.coinpurse.compact_str()

###################
# RP Prompt rolls #
###################

rp_msg = ""

final_check = (SkillRoll1.total + SkillRoll2.total) // 2

if final_check < DC_INDEX[0]:
    rp_msg = RP_PROMPTS["failure"][roll("1d15")-1]
elif final_check < DC_INDEX[1]:
    rp_msg = RP_PROMPTS["success"][roll("1d15")-1]
else:
    rp_msg = RP_PROMPTS["critical"][roll("1d20")-1]

################
# Final Result #
################

return f'''embed
            -title "Downtime Activity: Job"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {TIER})

**{skill1.capitalize()}:** {SkillRoll1}
**{skill2}:** {SkillRoll2}

__**Results:**__
**Coinpurse Changes:**
{COINPURSE_BEFORE} -> {COINPURSE_AFTER} (+{total_gold:.2f}gp)
**Exhaustion Streak:**
{before_exhaustion_streak} -> {exhaustion_streak}
{exh_msg}
**Optional Roleplay Prompt:**
{rp_msg}"""
            -thumb "{ch.image}"
            -footer "!dtd job [skill1] [skill2] | Athanor | !dtd help"
        '''