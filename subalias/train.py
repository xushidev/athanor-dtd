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
def train_dtd():
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

    # First use the default values
    if len(athanor_dtd["train_args"]) != 0:
        roll_arg1, roll_arg2, roll_arg3 = local_args["train_args"][0], local_args["train_args"][1], local_args["train_args"][2]
        bonus1, adv1 = roll_arg1
        bonus2, adv2 = roll_arg2
        bonus3, adv3 = roll_arg3

    # If the user adds arguments, override that
    # Parse arguments with context
    args = arguments.numargparse(&ARGS&)

    # Gets the bonuses / advantages for 1st roll
    args.set_context(1)
    bonus1, adv1 = 0 if args.get("none", False) else args.get("b", 0), 0 if args.get("none", False) else args.adv(eadv=True)

    # Gets the bonuses / advantages for 2nd roll
    args.set_context(2)
    bonus2, adv2 = 0 if args.get("none", False) else args.get("b", 0), 0 if args.get("none", False) else args.adv(eadv=True)

    # Gets the bonuses / advantages for 3rd roll
    args.set_context(3)
    bonus3, adv3 = 0 if args.get("none", False) else args.get("b", 0), 0 if args.get("none", False) else args.adv(eadv=True)
    # dis = -1, None = 0, adv = 1, eadv = 2

    # Stores them as tuple for easy deconstruction
    local_args["train_args"] = []
    local_args["train_args"].extend([(bonus1, adv1), (bonus2, adv2), (bonus3, adv3)])

    # Write new variables in cvar
    ch.set_cvar("athanor_dtd", dump_json(local_args))

    # Check for exhaustion and apply
    if exhaustion():
        # apply exhaustion
        adv1 -= 1
        adv2 -= 1
        adv3 -= 1
        adv1 = -1 if adv1 < -1 else adv1
        adv2 = -1 if adv2 < -1 else adv2
        adv3 = -1 if adv3 < -1 else adv3

    # Dice to roll table (adv, dis and eadv)
    dice = [
        "1d20",
        "2d20kh1",
        "3d20kh1",
        "2d20kl1",
    ]

    # Getting the highest score modifier
    atk_mod = max(strengthMod, dexterityMod, intelligenceMod, wisdomMod, charismaMod) + proficiencyBonus

    # Get the dices with advantage and disadvantage applied
    roll1 = dice[adv1]
    roll2 = dice[adv2]
    roll3 = dice[adv3]

    # Rolls
    if bonus1 == 0:
        atk_roll1 = vroll(f"{roll1} + {atk_mod}")
    else:
        bonuses = ""
        for bonus in bonus1:
            bonuses += "+" + bonus
        atk_roll1 = vroll(f"{roll1} + {atk_mod} {bonuses}")

    if bonus2 == 0:
        atk_roll2 = vroll(f"{roll2} + {atk_mod}")
    else:
        bonuses = ""
        for bonus in bonus2:
            bonuses += "+" + bonus
        atk_roll2 = vroll(f"{roll2} + {atk_mod} {bonuses}")

    if bonus3 == 0:
        dex_save = vroll(f"{roll3} + {ch.saves.get('dex')}")
    else:
        bonuses = ""
        for bonus in bonus3:
            bonuses += "+" + bonus
        dex_save = vroll(f"{roll3} + {ch.saves.get('dex')} {bonuses}")

    xp_roll1 = calculate_xp(atk_roll1.total)
    xp_roll2 = calculate_xp(atk_roll2.total)
    xp_roll3 = calculate_xp(dex_save.total)

    # Modify the coin purse and get the delta
    changes = ch.coinpurse.modify_coins(gp=int(-(global_args.get("level", level))))

    # Get the coinpurse after alias completion
    post_coins = ch.coinpurse.compact_str()

    # Return embed result
    return f'''embed
            -title "Downtime Activity: Train"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {(global_args.get("level", level))} | Tier {tier})

**First Attack Roll:** {atk_roll1}
**Second Attack Roll:** {atk_roll2}
**Dexterity Save**: {dex_save}

__**Results:**__
**Coinpurse Changes:**
{pre_coins} -> {post_coins} (-{(global_args.get("level", level)):.2f}gp)
**XP gained**:
{xp_roll1 + xp_roll2 + xp_roll3}XP | run `!xp +{xp_roll1 + xp_roll2 + xp_roll3} 'Combat Training'` in <#1043462883062861864>
**Exhaustion Streak:**
{pre_exhaustion} -> {post_exhaustion}
{get_random_exhaustion_rp()}"""
            -thumb "{ch.image}"
            -footer "!dtd train | Athanor | !dtd help"
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

return train_dtd()

</drac2>
