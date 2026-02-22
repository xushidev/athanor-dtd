############################
# Loading Custom Constants #
############################

VALID_SKILLS1 = ["medicine", "nature", "investigation", "survival", "animalHandling"]
VALID_SKILLS2 = ["sleightOfHand", "insight", "history", "persuasion", "perception"]

RP_PROMPTS = {
    "failure": [
        "...You realised too late that you forgot to wash your hands before applying the bandages, now you have to wash it and do it again, properly this time.",
        "Despite the patient's wishes, you continued the procedure, as painful as it sounds and looks.",
        "You underestimated your strength and tightened the bandage too much.",
        "You were too fast and did everything before anyone realised it happened, the patient magically healed and you were never acknowledged for your works.",
        "The tools betray you at the worst possible moment.",
        "The lack of money leaves you with little pay, as you had to do beneficiary work.",
        "Your effort are null as they didn't seem to work despite following the right procedures.",
        "The job technically worked, but not in the way anyone would consider a success.",
        "Someone else speaks first and takes credit, leaving you to explain what went wrong.",
        "You finish just a little too late, and that small delay makes all the difference.",
        "In trying to help, you reveal something you would have preferred to keep private.",
        "You complete the task, but the effort leaves you worse than when you started.",
        "Your idea makes sense on paper, yet falls apart the moment you apply it pratically.",
        "A small distraction breaks your concentration, and the mistake follows immediately.",
        "You do what was asked, only to be told you should have known better.",
        "You are fined slightly for a work done wrongly, you are lucky no life has been taken.",
        "You thought everything was going alright, but a professional comes and points out your mistakes.",
        "Where is your cap to prevent sweat from falling down?",
        "You talked... And talked... And talked... And the old lady left without doing anything, feeling better, but of course you didn't get paid for talking",
        "You inspire someone and pull them out from a dark mentality. But nobody acknowledges your effort.",
        "You run swiftly from a patient to another... And bump into someone.",
        "You bump into someone running too fast in the opposite direction."
    ],
    "success": [
        "You follow the correct steps, and this time they work as intended.",
        "The patient endures, and the procedure concludes without further complication.",
        "You keep a steady hand, and nothing slips out of place, fortunately.",
        "The tools cooperate, and that alone makes the difference.",
        "You finish without attracting attention, which is sometimes the best outcome.",
        "The employer pays you what was agreed, nothing more, nothing less.",
        "No one complains, and that is taken as approval.",
        "You correct a small mistake before it becomes visible on the patient.",
        "You leave the situation stable, if not improved.",
        "Your timing is precise enough to avoid further trouble.",
        "You feel the work was done properly, even if unnoticed.",
        "The result holds... at least for now.",
        "You are allowed to leave without questions.",
        "The process hurts, but it heals.",
        "You did what you were meant to do.",
        "The wounds is closed perfectly, nothing more and nothing less.",
        "A depressed person leaves you a tip as your speech with them leaves them much more willing to push on with life.",
        "You distract a patient enough for the medic to carry on a painful procedure.",
        "...You are left to write down all the informations about patients and which medicine to use in which condition."
    ],
    "critical": [
        "You anticipate the complication before it happens and adjust accordingly.",
        "The procedure succeeds so cleanly that no correction is needed.",
        "You fix an issue no one realised was there.",
        "The employer offers more work, trusting your steady hands, which means a bigger pay.",
        "Word spreads quietly about how well it went.",
        "Your method proves more efficient than expected.",
        "You turn a delicate situation into a controlled one.",
        "Someone important in the guild notices the precision of your work.",
        "The result lasts longer than anyone predicted.",
        "You gain the trust that is rarely given twice.",
        "The outcome prevents future problems before they arise.",
        "You make it look easier than it was.",
        "Your name is mentioned with respect and gratitude by the patient's family afterward.",
        "You leave behind something that will not need fixing for a while.",
        "You will be trusted with something more difficult next time.",
        "The recovery is faster than it should have been.",
        "Others ask how you managed to do it.",
        "You will be remembered for doing it right.",
        "The success feels earned.",
        "You feel warm in your chest watching the smile of your patient.",
        "The patient seems magically healed and you take the credit for it despite never doing anything",
        "The job becomes proof of your competence.",
        "Someone won't miss their family, you broke a circle of death by incompetence.",
        "A kind smile inspires you to keep up with the good work.",
        "A kid's laughter fills your ears with joy and happiness.",
        "\'I want to see the sky one more time... I want to feel the rays of the sun one more time...\' . . . \'Thank you. Kind person. You did the right thing.\'",
        "A burning sense of duty fills, as you watch over the tent filled with despair. You feel the need to fill it with HOPE"
    ]
}

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
if skill1 == "animalHandling":
    skill1 = "Animal Handling"
else:
    skill1 = skill1.capitalize()

if skill2 == "sleightOfHand":
    skill2 = "Sleight of Hand"
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
    rp_msg = RP_PROMPTS["failure"][roll("1d22")-1]
elif final_check < DC_INDEX[1]:
    rp_msg = RP_PROMPTS["success"][roll("1d19")-1]
else:
    rp_msg = RP_PROMPTS["critical"][roll("1d27")-1]

################
# Final Result #
################

return f'''embed
            -title "Downtime Activity: Medic"
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
            -footer "!dtd med [skill1] [skill2] | Athanor | !dtd help"
        '''