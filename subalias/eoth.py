<drac2>

# LIBRARIES
# Arguments, tools, progress bar
using(arguments="505f607f-d8cc-44bb-8a67-df5b871c95dd")
using(tool="6251e20c-7545-4c63-92af-31e0745f2b0c")
using(progress_bar="505f607f-d8cc-44bb-8a67-df5b871c95dd")

# Gets the character
ch = character()

# Gets a list of skills and tools
skills_list = [skill_name for (skill_name, skill) in ch.skills if skill_name not in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']]
tools_list = load_yaml(get_gvar('e65831da-1834-4089-9bbd-93fc36a2d622'))

global_args = arguments.numargparse(&ARGS&)

# Gets the tier of the character
tier = global_args.get("level", int(ch.levels.total_level//4.01+1))

# Gets the current time in Japan (+9 hours)
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
OFFSET = 9 * HOUR
TIME = floor(time() + OFFSET)

# Gold reward table
GOLD_INDEX = [
    {'pp': '0',   'gp': '1d2',  'sp': '1d4', 'cp': '1d8'},
    {'pp': '0',   'gp': '1d4',  'sp': '1d4', 'cp': '1d8'},
    {'pp': '0',   'gp': '1d6',  'sp': '1d4', 'cp': '2d4'},
    {'pp': '0',   'gp': '2d4',  'sp': '1d6', 'cp': '2d6'},
    {'pp': '0',   'gp': '2d6',  'sp': '1d2', 'cp': '1d4'},
    {'pp': '0',   'gp': '3d6',  'sp': '1d4', 'cp': '1d6'},
    {'pp': '0',   'gp': '4d6',  'sp': '2d4', 'cp': '2d6'},
    {'pp': '1d2', 'gp': '3d6',  'sp': '1d8', 'cp': '1d12'}
]

# Coinpurse before alias completion
pre_coins = ch.coinpurse.compact_str()

# Default athanor_dtd cvar to use
better_default = dump_json(
    {
        "last_dtd": 0,
        "exhaustion_streak": 0,
        "med_args": [],
        "job_args": [],
        "train_args": [],
        "eoth_args": []
    }
)
athanor_dtd = load_json(ch.get_cvar("athanor_dtd", better_default))

valid_skills = {
    "job": [
        ["acrobatics", "athletics", "stealth"],
        ["animalHandling", "deception", "intimidation", "investigation", "nature", "perception"]
    ],
    "med": [
        ["medicine", "nature", "investigation", "survival", "animalHandling"],
        ["sleightOfHand", "insight", "history", "persuasion", "perception"]
    ],
    "eoth": [
        ["carpenterstools", "masonstools", "glassblowerstools", "weaverstools", "cooksutensils", "herbalismkit"],
        ["persuasion", "medicine", "animalHandling", "nature", "arcana", "athletics"]
    ]
}

# Checks if no arguments is given:
args1 = '&1&'.lower()
args2 = '&2&'.lower()
no_args1 = '&' + '1' + '&'
no_args2 = '&' + '2' + '&'

def get_random_exhaustion_rp():
    if exhaustion():
        # Prompt for exhaustion
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
        # Returns a random prompt for exhaustion depending on the exhaustion streak
        exhaustion_message = "\n**Exhaustion:**\n"
        return exhaustion_message + EXHAUSTION_PROMPTS[roll("1d20")-1]
    else:
        return ""

def exhaustion():
    # check exhaustion, returns True or False depending on exhaustion streak
    if athanor_dtd["exhaustion_streak"] >= 4:
        return True
    return False

def roll_gold():
    gold = GOLD_INDEX[tier - 1]
    return (
        roll(gold["pp"]) * 10
        + roll(gold["gp"])
        + roll(gold["sp"]) / 10
        + roll(gold["cp"]) / 100
    )

def calculate_gold(skill_roll):
    if skill_roll.total < (8+(global_args.get("level", level)//2)+proficiencyBonus):
        # failure
        return roll_gold() - roll_gold()
    elif skill_roll.total < (8+(global_args.get("level", level))+proficiencyBonus):
        # success
        return roll_gold()
    else:
        # critical success
        return roll_gold() + roll_gold()

def calculate_xp(result_roll):
    die = (
            4 if result_roll.total < (8+(global_args.get("level", level)//2)+proficiencyBonus)
            else 6 if result_roll.total < (8+(global_args.get("level", level))+proficiencyBonus)
            else 8
        )
    return roll(f"{global_args.get('level', level)}d{die}")

# Downtime Activities available
def eotorath_dtd():
    # Variable to store the arguments given
    local_args = athanor_dtd.copy()

    # Get exhaustion before alias running
    pre_exhaustion = local_args["exhaustion_streak"]

    # Check time and add exhaustion to local_args
    if ((TIME // DAY) - (int(local_args["last_dtd"]) // DAY)) >= 2:
        local_args["exhaustion_streak"] = 0
    else:
        local_args["exhaustion_streak"] += 1

    # Get exhaustion after alias running
    post_exhaustion = local_args["exhaustion_streak"]

    # Log this as the last DTD done after having checked for exhaustion
    local_args["last_dtd"] = TIME

    # Parse arguments with context
    args = arguments.numargparse(&ARGS&)

    # Check if any inputs are given,
    # if we already have them, we use that
    # else it is error
    if (args1, args2) == (no_args1, no_args2) or args1 == "-choice":
        # If no skills are given, then we check the defaults
        if len(athanor_dtd["eoth_args"]) != 0:
            # If there are defaults, we use defaults (assume they are valid)
            args1, args2 = athanor_dtd["eoth_args"][0]
            skill1_arg, skill2_arg = athanor_dtd["eoth_args"][1]
            bonus1, adv1 = skill1_arg
            bonus2, adv2 = skill2_arg
        else:
            # If we don't have skills given and defaults, then it is an error
            return "echo Error: No input given"
    else:
        # If we have skills given by user
        # Gets the bonuses / advantages for 1st skill
        args.set_context(1)
        bonus1, adv1 = args.get("b", 0), args.adv()

        # Gets the bonuses / advantages for 2nd skill
        args.set_context(2)
        bonus2, adv2 = args.get("b", 0), args.adv()
        # dis = -1, None = 0, adv = 1, eadv = 2

        # Stores them as tuple for easy deconstruction
        local_args["eoth_args"] = []

        # Check if they are valid or not before writing
        # Search the exact skills in the arguments
        args1 = (tool.matching_tools(args1)+["default"])[0]
        args2 = ([x for x in skills_list if args2.lower().replace(' ', '') in x.lower()]+["default"])[0]

        # Checks if any of the arguments is "default"
        if {args1, args2} == {"default"}:
            return "echo Error: Invalid input"

        # Checks if the argument is in the valid skills
        if (args1 not in valid_skills["eoth"][0]) or (args2 not in valid_skills["eoth"][1]):
            return "echo Error: Invalid input"

        # If all the checks above pass, then add it to the defaults
        local_args["eoth_args"].extend([(args1, args2), ((bonus1, adv1), (bonus2, adv2))])

        # Write new variables in cvar
        ch.set_cvar("athanor_dtd", dump_json(local_args))

    # Get eventual rerolls from character (Halfling)
    reroll_number = ch.csettings.get("reroll", None)

    # Get reliable taleng or mc
    minimum_check1 = args.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[args1].prof>=1 else None)
    minimum_check2 = args.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[args2].prof>=1 else None)

    # Check for exhaustion and apply
    if exhaustion():
        # apply exhaustion
        adv1 -= 1
        adv2 -= 1
        adv1 = -1 if adv1 < -1 else adv1
        adv2 = -1 if adv2 < -1 else adv2

    # Roll the skills checks
    # Table to convert advantage:
    adv_table = {
        1: True,
        0: None,
        -1: False
    }

    # Roll the skill checks along with bonus
    if bonus1 == 0:
        skill_roll1 = vroll(tool.tool_check_dice_str(args1, base_adv=adv_table[adv1]))
    else:
        bonuses = ""
        for bonus in bonus1:
            bonuses += "+" + bonus
        skill_roll1 = vroll(f"{tool.tool_check_dice_str(args1, base_adv=adv_table[adv1])} {bonuses}")

    if bonus2 == 0:
        skill_roll2 = vroll(ch.skills[args2].d20(adv_table[adv2], reroll_number, minimum_check2))
    else:
        bonuses = ""
        for bonus in bonus2:
            bonuses += "+" + bonus
        skill_roll2 = vroll(f"{ch.skills[args2].d20(adv_table[adv2], reroll_number, minimum_check2)} {bonuses}")

    # Log repair progression
    combat_channel = combat()

    # Error if channel is not in combat
    if combat_channel is None:
        return "echo Error: not in combat"

    # Get the section choice and fuzzy find it
    choice = args.last("choice", None)
    choice = ([x.name for x in combat_channel.combatants if choice.lower().replace(' ', '') in x.name.lower()]+["default"])[0]

    # If the section choosen doesn't exist, then it is an error
    if choice == "default":
        return "echo Error: section not found"

    # Get the combatant of choice
    section = combat_channel.get_combatant(choice)

    # Check if the section is already complete
    if section.hp == section.max_hp:
        return "echo Error: section already complete"

    # Get the progression before
    pre_section = section.hp

    # Add and set the progress
    section.modify_hp(((skill_roll1.total + skill_roll2.total) // 2), overflow=False)

    complete_msg = ""

    if section.hp >= section.max_hp:
        # Completes the section and gives a message
        complete_msg = f"{choice} section is complete! Ping <@383474917556879370> to notify"

    # Get the progression after
    post_section = section.hp

    # Return embed result
    return f'''embed
            -title "Downtime Activity: Repair Eotorath"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {tier})

**{tool.tool_name_for(args1)}:** {skill_roll1}
**{args2.capitalize() if args2 != "animalHandling" else "Animal Handling"}:** {skill_roll2}

__**Results:**__
**Repair Progress:**
{pre_section}/{section.max_hp} -> {post_section}/{section.max_hp} (+{(skill_roll1.total + skill_roll2.total) // 2}) {complete_msg}
**Exhaustion Streak:**
{pre_exhaustion} -> {post_exhaustion}{get_random_exhaustion_rp()}"""
            -thumb "{ch.image}"
            -footer "!dtd eoth [tool1] [skill2] | Athanor | !dtd help"
        '''

# Check if it is using the old cvar or not, if it is, we update to the new schema
if athanor_dtd.get("default_skill1") != None:
    leg_last_dtd = athanor_dtd["last_dtd"]
    leg_exhaustion_streak = athanor_dtd["exhaustion_streak"]

    # Transfer old data
    new_schema = dump_json(
        {
            "last_dtd": leg_last_dtd,
            "exhaustion_streak": leg_exhaustion_streak,
            "med_args": [],
            "job_args": [],
            "train_args": [],
            "eoth_args": []
        }
    )

    # Write update to cvar
    ch.set_cvar("athanor_dtd", new_schema)

    # Update
    athanor_dtd = load_json(ch.get_cvar("athanor_dtd", better_default))

# Check the time, returns error directly if trying to do DTDs before reset.
if athanor_dtd["last_dtd"] != "":
    if (athanor_dtd["last_dtd"] // DAY) == (TIME // DAY):
        return f'echo You are doing 2 dtds in the same day, please try again tomorrow'

return job_dtd()

</drac2>
