<drac2>
#########################
# CONSTANTS definitions #
#########################

ch = character()

TIER = int(level//4.01+1)

TIME = floor(time())

a = argparse(&ARGS&)

# Get possible advantage from the arguments
adv = a.adv(boolwise=True)

DC_INDEX = [
    8+(level//2)+proficiencyBonus,
    8+level+proficiencyBonus
]

EXHAUSTION_PROMPTS = [
    "Your body refuses to cooperate; every movement feels heavier than the last. You need a full day of rest.",
    "Fatigue dulls your senses and slows your thoughts. Today is not a day for work.",
    "You wake up sore, drained, and unfocused. Pushing yourself further would be dangerous.",
    "Your muscles ache from overuse, protesting even simple tasks.",
    "Sleep clings to you no matter how hard you try to shake it. Productivity is impossible.",
    "Your hands tremble slightly, betraying how far you've pushed yourself.",
    "You feel worn down to the bone—rest is no longer optional.",
    "Every breath feels labored, and concentration slips away almost instantly.",
    "Your body demands recovery before it allows progress.",
    "You realize too late that you've overextended yourself. Today must be spent resting.",
    "Pain and fatigue cloud your judgment. Any serious effort would end badly.",
    "Your reflexes are slow, your thoughts sluggish. You need time to recover.",
    "Even routine tasks feel overwhelming; exhaustion has caught up with you.",
    "Your stamina is spent, and your body refuses further strain.",
    "You feel hollowed out, running on fumes. Rest is the only sensible option.",
    "Your limbs feel leaden, and your mind struggles to stay focused.",
    "Ignoring your exhaustion now would risk injury or worse.",
    "You recognize the warning signs—your body needs a full day to recover.",
    "Sleep comes easily, but waking up feels just as heavy. Today must be rest.",
    "Your exhaustion is obvious to anyone who looks at you. You need time to recover."
]

#################
# Loading cvars #
#################

default = dump_json(
    {
        "last_dtd": "",
        "exhaustion_streak": 0,
        "default_skill1": "",
        "default_skill2": ""
    }
)
athanor_dtd = load_json(ch.get_cvar("athanor_dtd", default))

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

########################
# Exhaustion penalties #
########################

exh_msg = ""

if exhaustion_streak > 4:
    exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
    match adv:
        case None:
            adv = False
        case True:
            adv = None
        case _:
            # do nothing (can't eadv or go below dis)
            adv = adv

#########################
# Combat Training rolls #
#########################

# We don't have need for additional arguments other than simply advantage and such

# getting the highest modifier between: strength, dexterity, intelligence, wisdom and charisma
atk_mod = max(strengthMod, dexterityMod, intelligenceMod, wisdomMod, charismaMod) + proficiencyBonus

dice = "1d20"
if adv:
    dice = "2d20kh1"
elif adv == False:
    dice = "2d20kl1"
else:
    dice = "1d20"

atk_roll1 = vroll(f"{dice} + {atk_mod}")
atk_roll2 = vroll(f"{dice} + {atk_mod}")

dex_mod = ch.saves.get("dex")

dex_save = vroll(dex_mod.d20(adv))

############
# XP rolls #
############

xp_roll1 = 0
xp_roll2 = 0
xp_roll3 = 0

if atk_roll1.total < DC_INDEX[0]:
    # fail
    xp_roll1 = roll(f"{level}d4") - roll(f"{level}d4")
elif atk_roll1.total < DC_INDEX[1]:
    # success
    xp_roll1 = roll(f"{level}d4")
else:
    # critical success
    xp_roll1 = roll(f"{level}d4") + roll(f"{level}d4")

if atk_roll2.total < DC_INDEX[0]:
    # fail
    xp_roll2 = roll(f"{level}d4") - roll(f"{level}d4")
elif atk_roll2.total < DC_INDEX[1]:
    # success
    xp_roll2 = roll(f"{level}d4")
else:
    # critical success
    xp_roll2 = roll(f"{level}d4") + roll(f"{level}d4")

if dex_save.total < DC_INDEX[0]:
    # fail
    xp_roll3 = roll(f"{level}d4") - roll(f"{level}d4")
elif dex_save.total < DC_INDEX[1]:
    # success
    xp_roll3 = roll(f"{level}d4")
else:
    # critical success
    xp_roll3 = roll(f"{level}d4") + roll(f"{level}d4")

# tier as modifier
total = (xp_roll1 + xp_roll2 + xp_roll3) * TIER

if total < 0:
    total = 0

################
# Final Result #
################

return f'''embed
            -title "Job downtime"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {TIER})

**First Attack Roll:** {atk_roll1}
**Second Attack Roll:** {atk_roll2}
**Dexterity Save**: {dex_save}

__**Results:**__
**XP gained**:
{total}XP | run `!xp +{total} 'Combat Training'` in <#1043462883062861864>
**Exhaustion Streak:**
{before_exhaustion_streak} -> {exhaustion_streak}
{exh_msg}"""
            -thumb "{ch.image}"
            -footer "Athanor"
        '''
</drac2>